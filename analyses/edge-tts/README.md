# Edge-TTS

Reverse-engineered Python client for Microsoft Edge's "Read Aloud" TTS websocket.

- **Upstream:** <https://github.com/rany2/edge-tts>
- **Analyzed release:** `7.2.8` (2026-03-22)
- **Snapshot:** `sources/edge-tts/` — full `git fetch --tags --unshallow` of upstream (314 commits, 12 tags, 4 branches), detached at `7.2.8`
- **Off-repo backups** (in case upstream disappears):
  - `sources/edge-tts.bundle` — 2.2 MB git bundle with `--all`, sha256 `0a1a0c8dba5b03d05bc4bf9ebbff0d6adab4e3112d2aca53590253c7febdb8c9`
  - `sources/edge-tts-7.2.8.tar.gz` — 125 KB source tarball (no .git), sha256 `684f6ffa04bfa4f46505ff524090366b061fa3578b3b65cb941a1c9589b82221`
- **Analysis:** `analysis.md`
- **Analyzed:** 2026-09-27

## Rebuild from backup

If the live clone is broken and the upstream repo is gone:

```bash
# From git bundle (preserves full history + tags + branches)
git clone /path/to/edge-tts.bundle restored/edge-tts
cd restored/edge-tts && git checkout 7.2.8

# From tarball (just the source tree, no history)
mkdir restored/edge-tts && tar -xzf edge-tts-7.2.8.tar.gz -C restored/edge-tts
```

## Files

| Path | What it is |
| --- | --- |
| `analysis.md` | Architecture, protocol, API surface, risk analysis, release history, design notes |
| `../../sources/edge-tts/` | Full source tree of upstream at tag `7.2.8` (read-only snapshot) |

## TL;DR from the analysis

Pure-Python client to `speech.platform.bing.com`. ~6.6 M downloads/month, 12 k
stars. No API key needed. Solid for personal / OSS / research use; risky for
commercial SLAs because MS rotates the `TRUSTED_CLIENT_TOKEN` and
`CHROMIUM_FULL_VERSION` roughly every quarter (release history shows 5 patches
between 2025-08 and 2026-03 alone).

The biggest correctness change (PR #468) replaced metadata-based offset
compensation with byte-count math against the CBR 48 kbps mono MP3 stream —
subtitle timings are now monotonic for any text length.