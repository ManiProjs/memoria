# Memoria

Search your past.

## What is this?

Memoria is a second memory for you. It takes screenshots so you search for them with OCR

Memoria is also a Microsoft (Or in other words, Microslop)'s Windows Recall alternative for Windows, macOS and Linux.

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

For the frontend, you need the following:

- [Node.js](https://nodejs.org)
- [npm (which comes preinstalled with Node.js)](https://npmjs.com)
`cd` into the `memoria-ui` directory.

Then install the required packages for frontend.

```shell
npm install
```

Then,

```shell
npm run build
```

And finally,

```shell
npm run preview
```

Visit the app by going into [http://localhost:4173](http://localhost:4173).

## API Guide

For API guide, visit [APIS.md](./APIS.md)
