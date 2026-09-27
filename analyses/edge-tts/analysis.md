# rany2/edge-tts — deep analysis

Snapshot date: 2026-09-27 (analysis run). Repo state at master = release tag `7.2.8` (2026-03-22).

## TL;DR

Pure-Python client for Microsoft Edge's "Read Aloud" TTS websocket
(`speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1`).
No API key, no Edge browser, no Windows required. LGPLv3 (`srt_composer.py`
is MIT, derived from `cdown/srt`).

- Repo: 12,076 stars / 1,115 forks / 80 watchers / 3 open issues / 2,210 KB.
- PyPI `7.2.8`, requires Python `>=3.7`, 67 releases total.
- PyPI downloads (no mirrors, `pypistats.org`):
  - last day: 306,600
  - last week: 1,865,359
  - last month: 6,614,715
  - trailing ~180 d: 48,935,044

## Architecture (1,890 LOC)

```
src/edge_tts/                 # core library
  __init__.py         public surface: Communicate, SubMaker, VoicesManager, list_voices
  __main__.py         → util.main
  communicate.py      658 LOC  WS client, split_text_by_byte_length, mkssml, Communicate
  voices.py           122 LOC  voices list HTTP GET + VoicesManager.find()
  drm.py              160 LOC  Sec-MS-GEC token + clock-skew correction + MUID
  constants.py         45 LOC  endpoints, headers, TRUSTED_CLIENT_TOKEN, CHROMIUM_FULL_VERSION
  data_classes.py      91 LOC  TTSConfig (regex validation), UtilArgs
  typing.py            62 LOC  TypedDicts: TTSChunk, Voice, VoicesManagerVoice, CommunicateState
  submaker.py          60 LOC  SubMaker -> WordBoundary/SentenceBoundary -> SRT
  srt_composer.py     294 LOC  MIT-licensed fork of cdown/srt
  util.py             145 LOC  argparse CLI: edge-tts
  exceptions.py        28 LOC  EdgeTTSException hierarchy
  version.py            4 LOC  __version__ = "7.2.8"
src/edge_playback/            # optional mpv / winsound wrapper
  __main__.py         130 LOC  _parse_args, _check_deps, _run_edge_tts, _play_media
  win32_playback.py    52 LOC  ctypes mciSendStringW MP3 playback
```

## Protocol — the meat

### Endpoints (`constants.py`)
- WSS: `wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?TrustedClientToken=6A5AA1D4EAFF4E9FB37E23D68491D6F4`
- Voice list HTTPS: `https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list?trustedclienttoken=…`
- Output format hard-coded: `audio-24khz-48kbitrate-mono-mp3` (CBR 48 kbps mono).

### DRM token (`drm.py`)
- `generate_sec_ms_gec()`: SHA-256 of
  `{windows-filetime-ticks-rounded-down-to-5-min}{TRUSTED_CLIENT_TOKEN}`,
  uppercased. Windows filetime = `(unix + 11644473600) * 1e7`.
  Regenerated every 5 min because of the round-down.
- MUID: random `secrets.token_hex(16)` injected as `Cookie: muid=…;`.
- `clock_skew_seconds` class attribute auto-corrects from the `Date:`
  response header on 403 (only the voices list path; `stream()` retries
  inside its own 403 handler).
- WSS URL carries `Sec-MS-GEC`, `Sec-MS-GEC-Version`
  (e.g. `1-143.0.3650.75`), `ConnectionId`.

### SSML construction (`mkssml`)
- Hard-coded `xml:lang='en-US'` (locale is inferred from the voice short
  name, not propagated to the SSML root).
- Single envelope:
  `<voice name='Microsoft Server Speech Text to Speech Voice (lang-REGION, NameNeural)'><prosody pitch= rate= volume=…>`.
  Custom SSML is unsupported — server rejects anything beyond this prosody.
- `TTSConfig.__post_init__` coerces `en-US-EmmaMultilingualNeural` →
  `Microsoft Server Speech Text to Speech Voice (en-US, EmmaMultilingualNeural)`.

### WebSocket session (`Communicate.__stream`)
1. Open `aiohttp` WS (`compress=15`, optional `proxy`,
   `ClientTimeout(sock_connect=10, sock_read=60)`).
2. Send config frame with `metadataoptions.sentenceBoundaryEnabled` /
   `wordBoundaryEnabled` toggled per `boundary` argument (default
   `SentenceBoundary`); `outputFormat` hard-coded.
3. Loop messages:
   - TEXT frame → header has `Path: audio.metadata` or `turn.end`.
     Metadata yields `{type, offset, duration, text}` after `unescape()`
     (MS ships XML-escaped text inside JSON — caught by #378).
   - BINARY frame → first 2 bytes = big-endian header length; body is
     `audio/mpeg`. Each audio chunk is appended to
     `state.chunk_audio_bytes` and yielded.
4. On `turn.end` → `__compensate_offset()`. Any other `Path` →
   `UnknownResponse`.
5. If no audio frame was ever yielded → `NoAudioReceived`.

### Long-text handling
- `split_text_by_byte_length(text, 4096)`: prioritises
  newline → space → safe UTF-8 boundary → XML-entity-aware fallback
  (`_adjust_split_point_for_xml_entity` prevents splitting `&amp;`).
- Iterates one `<=4096 B` chunk per WS round-trip, each yielding audio
  + boundary events.
- Removes control chars `0x00-0x08, 0x0B-0x0C, 0x0E-0x1F`
  (esp. `\v` from OCR PDFs).

### Offset-drift fix (PR #468, the big correctness change)
Previous code accumulated `offset_compensation` from server-reported
metadata offsets + a hard-coded 8,750,000-tick padding. Long texts drifted
because MS reports integer overflows and AI inserts variable silence.
New approach: since output is CBR 48 kbps mono MP3, byte count maps to
ticks exactly:
```
ticks = total_bytes * 8 * 10_000_000 // 48_000
```
`__compensate_offset()` runs after every `turn.end`, resetting
`chunk_audio_bytes` for the next chunk. Subtitle timings are monotonic
for any text length.

## Public API

| Surface                 | Sync                                  | Async                                            |
| ----------------------- | ------------------------------------- | ------------------------------------------------ |
| Save full audio (+ JSON) | `save_sync(path, metadata_path=None)` | `await save(path, metadata_path=None)`           |
| Iterate chunks          | `stream_sync()` (ThreadPoolExecutor + new event loop + queue) | `async for chunk in stream()` |
| List voices             | —                                     | `await list_voices(proxy=…)`                     |
| Find voices             | —                                     | `VoicesManager.create()` → `find(Gender, Locale, Language)` |
| Subtitles               | `SubMaker().feed(chunk).get_srt()` (or `__str__`) | same |
| DRM helpers             | `DRM.generate_sec_ms_gec / generate_muid / headers_with_muid / adj_clock_skew_seconds / parse_rfc2616_date / handle_client_response_error` | same |

`TTSChunk.type` ∈ `Literal["audio", "WordBoundary", "SentenceBoundary"]`.
Audio carries `bytes data`; boundaries carry `offset` (100 ns ticks,
already compensated) + `duration` + `text`.

## CLI

`edge-tts -t TEXT | -f FILE | -l [--voice] [--rate] [--volume] [--pitch]
[--write-media] [--write-subtitles] [--proxy]`.

`edge-playback` shells out to `edge-tts`, then spawns `mpv` with
`--sub-file` (or `mciSendStringW` on Windows).

## Tests

A single shell script `tests/001-long-text.sh`:
- Runs `edge-tts -f tests/001-long-text.txt` ×26 in parallel (`a..z`).
- Asserts all 25 produced `.srt` files are byte-identical via `cmp`
  against the `a` baseline.

This is the regression guard for the CBR offset fix. No `pytest` or
`unittest` in the repo.

CI (`.github/workflows`):
- `code-quality.yml`: mypy + pylint + isort + black on push and PR.
- `codeql-analysis.yml`: weekly + push/PR CodeQL Python scan.

## Release / change cadence (last 6 months)

- **2025-08-05** `7.1.0` → `7.2.0`:
  `SentenceBoundary` default, drop `merge_cues`, bundle `srt_composer`,
  4096 B chunk limit (#394).
- **2025-08-20** `7.2.1`: Py3.7 `dict.items()` fix.
- **2025-08-28** `7.2.2` → `7.2.3`: Edge Chromium bumped to
  `140.0.3485.14`; **endpoint migration** (#412) — voices list URL
  flipped, broke `7.2.0/1`.
- **2025-12-11** `7.2.4` → `7.2.6`: Endpoint broke again (#445),
  `MUID` support added, `--version` flag (#423), revert to current
  Edge endpoint.
- **2026-03-22** `7.2.7` → `7.2.8`: PR #468 (CBR offset compensation),
  PR #469 (cache SSL context at module level → ~250 ms saved per call),
  PR #470 (`HTTPS_PROXY` env var), PR #474 (`NoAudioReceived` now
  includes WS message types in the diagnostic).

## Open issues (3)

- **#482** `.WSServerHandshakeError: 503` (2026-07-21) — server flake.
- **#481** `"NoAudioReceived"` in Armenian / Punjabi / Basque
  (2026-07-20) — likely locale/voice metadata gap.
- **#473** Intermittent "No audio was received" with valid requests
  (2026-04-08).

Adjacent closed issues:
- **#483** License clarification (LGPL-3.0-only vs `-or-later`) —
  closed 2026-07-31, resolved by LICENSE top-of-file.
- **#477** RFC "Multimodal Production-Grade TTS Platform" — closed,
  not taken.

## Design choices / risks

1. **Reverse-engineered private endpoint.** No contract from MS;
   project lives at the mercy of `speech.platform.bing.com`
   URL/version changes. Recent history shows ~1 break per quarter.
2. **`TRUSTED_CLIENT_TOKEN` is hard-coded.** If MS rotates it, the
   library goes dark until the next release. `CHROMIUM_FULL_VERSION`
   (currently `143.0.3650.75`) is the other rotation point.
3. **Sec-MS-GEC has 5-minute granularity.** Long-running batch jobs
   may cross a boundary; the token is regenerated per
   `Communicate.stream()` call, not cached.
4. **`trust_env=True` + `HTTPS_PROXY`** behaviour fixed in #470.
5. **SSL context cached at module level since 7.2.8** — saves
   ~250 ms per call. Module-level state is shared across event loops.
6. **`stream_sync()` spawns a fresh `asyncio.new_event_loop`** per
   call inside a thread pool — not safe to call concurrently from
   the same process. Concurrent sync calls each get their own loop,
   but reusing a `Communicate` after `stream_sync` will mis-state
   `stream_was_called`.
7. **`xml:lang='en-US'` is hard-coded** in `mkssml` even for non-en
   voices. Server still routes via the voice name; the SSML lang tag
   is informational only here.
8. **MIT/LGPL split** is documented at the top of LICENSE but not in
   `setup.py` `classifiers` — #483 was raised exactly because of this.
9. **Two sync wrappers, two strategies**: `save_sync()` runs
   `asyncio.run(self.save(...))` in a worker; `stream_sync()` builds
   its own queue + loop. Same class, different paths.
10. **No retry on `NoAudioReceived`** other than the 403 clock-skew
    case — it surfaces as a hard error.

## Is it usable?

Yes, with caveats:

| Use case | Verdict |
| --- | --- |
| Personal / OSS / research / internal tools | Drop-in. The most mature Python client for free Edge TTS. |
| Voice assistants, podcast generation, narration pipelines | Solid — `SubMaker` + CBR-correct offsets make it subtitle-safe. |
| Commercial product TTS (SLAs) | Risky — endpoint breaks ~quarterly, no upstream SLA. Plan for fallback (Azure Speech, gTTS, Piper, ElevenLabs). |
| Long-running batch (>1 h, 5-min token granularity) | Fine — token regenerates per `stream()` call. |
| Strict offline / air-gapped | No — requires live WS to `speech.platform.bing.com`. |

Operational rules of thumb:

- Use `await communicate.stream()` inside an existing event loop;
  don't call `stream_sync()` from inside one.
- Re-use a single `VoicesManager.create()` across many `Communicate`
  instances — list fetch is one HTTP round-trip.
- Pass `connector` if you need connection pooling or custom DNS;
  pass `proxy` only when needed — `trust_env=True` already picks up
  `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`.
- `connect_timeout` / `receive_timeout` default to 10 s / 60 s —
  bump for very long chunks.
- `boundary="WordBoundary"` yields per-word timestamps (good for
  karaoke); `SentenceBoundary` is the subtitle-friendly default.
- For SRT correctness on long text, use `SubMaker` rather than
  rolling your own — it's covered by #468.
- If MS rotates `CHROMIUM_FULL_VERSION` or `TRUSTED_CLIENT_TOKEN`,
  watch for `WSServerHandshakeError: 403` or `Sec-MS-GEC token
  rejected`. Fix is upstream; pin only after the dust settles.

## Notable downstream usage

- `hass-edge-tts` — Home Assistant TTS integration.
- `Podcastfy` — multi-source podcast generator.
- `openedai-speech` — local OpenAI-compatible TTS drop-in.
- `tts-samples`, `tts-with-rvc-onnx`.
- `elizaos-plugin-edge-tts`, `ovos-tts-plugin-edge-tts`.
- `edge-tts-ext`, npm `edge-tts` (Node port, ~5-6 direct dependents).

## Empirical verification (2026-09-27)

Installed `edge-tts==7.2.8` into a throwaway `python3 -m venv` and ran
the following against the live `speech.platform.bing.com` endpoint.
All temp artifacts (`/tmp/edge-tts-venv`, `/tmp/edge-tts-test`) were
deleted after testing — zero residue in system Python.

| Test | Result |
| --- | --- |
| `--list-voices` | OK — 5.16 s, voices endpoint reachable, DRM token + clock-skew path works. |
| Short text MP3 | OK — `MPEG ADTS, layer III, v2, 48 kbps, 24 kHz, Monaural` (matches hard-coded `audio-24khz-48kbitrate-mono-mp3`). |
| Streaming + SRT (`SentenceBoundary`) | OK — 3 sentences, timestamps continuous (50ms → 1237ms → 2287ms → 4712ms). |
| WordBoundary via `Communicate(boundary="WordBoundary")` | OK — 8 words with per-word offsets, sub_type correctly tracked. |
| `--rate=-30% --pitch=-10Hz --volume=+20%` | OK — MP3 still CBR 48 kbps; prosody changes synthesis, not encoding. |
| Chinese `zh-CN-YunjianNeural` | OK — sentence SRT continuous, MP3 48 kbps. |
| **PR #468 CBR math** (bytes ↔ ffprobe duration) | OK — short text 2.088s, long text 60.264s, **0 ms diff, 0.000% error**. |

### Bug surfaced by testing — SRT / MP3 are not deterministic across runs

Ran the upstream regression shape (10 parallel `edge-tts -f` invocations
of the same text):

- All 10 produced valid SRT files with the same content.
- All 10 SRT files differed byte-for-byte — sentence boundary offsets
  drift ±50–100 ms between invocations.
- MP3 files differ in size by up to 1,584 bytes (≈264 ms of audio)
  between invocations of the same text.
- Audio content itself is audibly identical (same voice, same text)
  but the AI inserts variable inter-sentence silence that varies
  per request.

Implications:

- The upstream `tests/001-long-text.sh` regression is **flaky** in
  practice. If it passes locally, it's mostly luck (same network,
  same token window, similar timing).
- `SubMaker` is fine for one-shot subtitle generation. It is **not**
  a stable artifact for caching, snapshot testing, or content
  addressing.
- For reproducible output, batch the same `Communicate` instance
  and stick with one connection per text rather than 26 parallel
  fan-outs.

This is consistent with the analysis above — `SentenceBoundary`
offsets come from MS-reported metadata, not from the deterministic
CBR byte count. PR #468 fixed the long-text drift *within* a single
stream; it did not (and cannot) make two separate streams agree
byte-for-byte.

## Usage (validated 2026-09-27)

After listening to eight live samples (Chinese Mandarin F/M, Chinese
Hunan-na, English F/M, Cantonese F/M), the selected voice for our use
case is **`zh-HK-HiuGaaiNeural`** — female, Cantonese (Hong Kong).
Reasoning:

- Native HK Cantonese pronunciation on traditional-Chinese text
  (粤拼 tones preserved; "嘅"/"哋"/"唔"/"啲" read correctly, not
  fallback-Mandarin).
- Female, mid-pitch, conversational pace — fits narration /
  explainer / YouTube voice-over.
- Among the three `zh-HK-*` voices, HiuGaai outperformed HiuMaan
  (faster, less natural) and WanLung (male, deeper) for our needs.

### Operational recipe

Run from a throwaway venv; never install `edge-tts` into the system
Python. Output goes to a temp dir, deleted after the run.

```bash
# 1. isolate
python3 -m venv /tmp/tts-venv
/tmp/tts-venv/bin/pip install edge-tts==7.2.8

# 2. generate (single file, no SRT)
TEXT="今日天氣唔錯,我哋一齊去飲茶。"
/tmp/tts-venv/bin/edge-tts \
    --voice zh-HK-HiuGaaiNeural \
    --text "$TEXT" \
    --write-media /tmp/tts-out.mp3

# 3. generate with SRT (for video subtitle track)
/tmp/tts-venv/bin/edge-tts \
    --voice zh-HK-HiuGaaiNeural \
    --text "$TEXT" \
    --write-media /tmp/tts-out.mp3 \
    --write-subtitles /tmp/tts-out.srt

# 4. tweak prosody — slower, slightly higher pitch, louder
/tmp/tts-venv/bin/edge-tts \
    --voice zh-HK-HiuGaaiNeural \
    --rate=-15% --pitch=+5Hz --volume=+10% \
    --text "$TEXT" \
    --write-media /tmp/tts-out.mp3

# 5. long text — let the 4096-byte splitter do its job; SRT stays
#    monotonic for the duration of one stream (PR #468).
#    But two separate invocations of the same text will produce
#    byte-different outputs (see "Bug surfaced" above).

# 6. cleanup
rm -rf /tmp/tts-venv /tmp/tts-out.*
```

### Programmatic recipe (when wrapping into a script)

```python
import asyncio, edge_tts

VOICE = "zh-HK-HiuGaaiNeural"

async def synth(text: str, mp3_path: str, srt_path: str | None = None):
    comm = edge_tts.Communicate(
        text,
        VOICE,
        rate="-15%", pitch="+5Hz", volume="+10%",
        boundary="SentenceBoundary",  # or "WordBoundary" for karaoke
    )
    sub = edge_tts.SubMaker()
    audio = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
            sub.feed(chunk)
    with open(mp3_path, "wb") as f:
        f.write(audio)
    if srt_path:
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(sub.get_srt())

asyncio.run(synth("今日天氣唔錯。", "/tmp/out.mp3", "/tmp/out.srt"))
```

### Voice catalog (validated from `VoicesManager.create()`)

Total: **322 voices** across 130+ locales. The ones that mattered for
our pick:

| Voice | Locale | Gender | Why considered |
| --- | --- | --- | --- |
| `zh-CN-XiaoxiaoNeural` | zh-CN | F | Mandarin baseline — friendly/warm |
| `zh-CN-YunjianNeural` | zh-CN | M | Mandarin — narrative/deep |
| `zh-CN-XiaoyiNeural` | zh-CN | F | Mandarin — lively |
| `zh-CN-liaoning-XiaobeiNeural` | zh-CN-liaoning | F | 东北话 Mandarin dialect — humorous |
| `zh-CN-shaanxi-XiaoniNeural` | zh-CN-shaanxi | F | 陕西话 Mandarin dialect — bright |
| `en-US-EmmaMultilingualNeural` | en-US | F | English default — multilingual |
| `en-US-GuyNeural` | en-US | M | English — passionate |
| `zh-HK-HiuGaaiNeural` | zh-HK | F | **Selected** — HK Cantonese |
| `zh-HK-HiuMaanNeural` | zh-HK | F | HK Cantonese — alt, faster |
| `zh-HK-WanLungNeural` | zh-HK | M | HK Cantonese — male |
| `zh-TW-HsiaoChenNeural` | zh-TW | F | 台湾国语 — female |
| `zh-TW-YunJheNeural` | zh-TW | M | 台湾国语 — male |

**Notable absences** (not in the upstream voice list):

- No Hunan / 湘语 / 湖南话 voice. Even at Azure TTS the Hunan dialect
  isn't offered as a discrete voice — `zh-CN-liaoning` (东北) and
  `zh-CN-shaanxi` (陕西) are the only Mandarin dialect voices.
- No way to pick SSML `<mstts:express-as style="…">` via this client
  (server rejects custom SSML beyond the single `<prosody>` envelope).
- No voice cloning / fine-tuning API — this is a thin wrapper over a
  fixed Azure voice catalog.

## Sources

- https://github.com/rany2/edge-tts (repo metadata, issues, PRs, events)
- https://pypi.org/project/edge-tts/ (release metadata)
- https://pypistats.org/api/packages/edge-tts/{recent,overall} (downloads)
- Raw files at `master`:
  `__init__.py`, `__main__.py`, `communicate.py`, `voices.py`,
  `drm.py`, `constants.py`, `data_classes.py`, `typing.py`,
  `submaker.py`, `srt_composer.py`, `util.py`, `exceptions.py`,
  `version.py`, `edge_playback/__main__.py`,
  `edge_playback/win32_playback.py`,
  `.github/workflows/{code-quality,codeql-analysis}.yml`,
  `tests/001-long-text.sh`, `setup.cfg`, `setup.py`, `LICENSE`.
- **Live verification**: `pip install edge-tts==7.2.8` into
  `/tmp/edge-tts-venv` (Python 3.14.7), tested against the live
  endpoint on 2026-09-27, env deleted after testing.