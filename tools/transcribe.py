#!/usr/bin/env python
"""Transcribe voice-memo audio files from a folder with faster-whisper.

Usage:
  python tools/transcribe.py "G:\\My Drive\\Pictures\\2026 Sri Lanka Ella & Arugam Bay"

Transcribes every audio file (.m4a/.mp3/.wav/.aac/.ogg/.flac) in the folder,
writing a <name>.txt next to each one. Skips files that already have an
up-to-date .txt so it's safe to re-run as more memos are added.
"""
import sys
import os
import glob

from faster_whisper import WhisperModel

MODEL_DIR = r"C:\Users\agile\whisper-small"
AUDIO_EXTS = (".m4a", ".mp4a", ".mp3", ".wav", ".aac", ".ogg", ".flac")


def transcribe_file(model, path):
    segments, info = model.transcribe(path, vad_filter=True)
    lang = info.language
    parts = []
    for seg in segments:
        parts.append(seg.text.strip())
    text = " ".join(p for p in parts if p).strip()
    return lang, text


def main():
    if len(sys.argv) < 2:
        print("usage: transcribe.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print("not a folder:", folder)
        sys.exit(1)

    files = []
    for ext in AUDIO_EXTS:
        files.extend(glob.glob(os.path.join(folder, "*" + ext)))
        files.extend(glob.glob(os.path.join(folder, "*" + ext.upper())))
    files = sorted(set(files))
    if not files:
        print("no audio files found in", folder)
        return

    print(f"Loading model from {MODEL_DIR} ...")
    model = WhisperModel(MODEL_DIR, device="cpu", compute_type="int8")

    for path in files:
        out = os.path.splitext(path)[0] + ".txt"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(path):
            print("skip (up to date):", os.path.basename(path))
            continue
        print("transcribing:", os.path.basename(path))
        lang, text = transcribe_file(model, path)
        with open(out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        preview = text[:200] + ("..." if len(text) > 200 else "")
        print(f"  [{lang}] -> {os.path.basename(out)}")
        print(f"  {preview}\n")


if __name__ == "__main__":
    main()
