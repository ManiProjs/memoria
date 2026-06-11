# Memoria

Search your past.

## What is this?

Memoria is a second memory for you. It takes screenshots so you search for them with OCR

Memoria is also a Microsoft's Windows Recall alternative for Windows, macOS and Linux.

### System Requirements

You don't need a powerful computer or an NPU. You just need:

- [Python](https://python.org/)
- [uv](https://docs.astral.sh/uv)
- [Git](https://git-scm.com/)
- [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)

Currently, you need to clone this repository, then `cd` to backend directory and run

```shell
uv run uvicorn app.main:app --reload --port 8009
```

We don't have a GUI yet.

For API guide, visit [APIS.md](./APIS.md)
