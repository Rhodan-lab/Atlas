if (!globalThis.CSS) globalThis.CSS = {};
if (!globalThis.CSS.escape) {
  globalThis.CSS.escape = value => String(value).replace(
    /[^a-zA-Z0-9_-]/g,
    character => `\\${character.codePointAt(0).toString(16)} `,
  );
}
