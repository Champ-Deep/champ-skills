# Local GLB import gates

Validate the JSON-level facts **before** `GLTFLoader` parses the buffer. A post-parse vertex count runs only after the expensive traversal has already happened, so it cannot protect the tab it is meant to protect.

## Header and chunk framing

- Magic `glTF`, version 2, declared length equals the buffer byte length.
- JSON chunk type with a 4-byte aligned length, inside bounds.
- Every following chunk: 4-byte aligned length, inside bounds, binary type. Walk all of them, do not assume a single trailing chunk.
- Parse the JSON and reject on failure before touching anything else.

## Reject before the loader

- Any `uri` that is not a `data:` URL, meaning relative paths, protocol-relative `//host`, `http(s):` and `file:`. This is the local-only guarantee.
- `data:` URIs only with a media-type allowlist: `application/octet-stream`, `application/gltf-buffer`, `image/png`, `image/jpeg`, `image/webp`. An unfiltered `data:` accepts `text/html` and other types nobody intended to ship.
- Any entry in `extensionsRequired` outside an explicit allowlist, such as `KHR_materials_unlit`, `KHR_mesh_quantization`, `KHR_texture_transform`. The loader only warns about unknown required extensions and keeps going, so the model renders wrong geometry in silence. Throw instead.
- Compression extensions (Draco, KTX/Basis, Meshopt) unless their decoders were deliberately bundled. Shipping a decoder is a supply-chain decision, not a default.

## Complexity starting caps

Tune these to the largest trusted model, then hold them.

| Field | Cap |
|---|---|
| nodes | 2048 |
| meshes | 512 |
| materials | 512 |
| images | 32 |
| textures | 64 |
| skins | 64 |
| accessors, bufferViews | 4096 each |

- Each accessor `count` a non-negative safe integer, at most 1,500,000; total accessor elements at most 12,000,000.
- Summed skin joints at most 4096.
- Node hierarchy: every node reachable, depth at most 128, no cycles (active-set depth-first walk). A cycle or a dangling child index is a hang or a crash, not a warning.
- Metadata nesting depth at most 128.
- Total file size capped at the input control, before the file is even read.

## Defense in depth

1. The validator above, on the `ArrayBuffer`.
2. A `LoadingManager.setURLModifier` that throws on anything not `blob:` or `data:` while parsing from the buffer.
3. Page CSP with `connect-src 'self' blob: data:`, so even a bypassed check cannot leave.

All three are cheap. Keep them: each one has a different failure mode.

## Display rules that keep an import honest

- Center and scale the model to a display height, and label it display-scaled, never measured.
- While an import is loaded, disable the controls that would imply registration: tissue sliders, layer presets, cutaway. Relabel the model banner to say the surface is not registered to the reference anatomy.
- Dispose the previous import's geometries, materials and textures on replace and on removal, or every swap leaks GPU memory.
- The exit path must restore a visible, selectable layer rather than assuming the skin layer is still on; picking a hidden structure leaves the inspector claiming something the dropdown cannot show.
- Cap vertices after load as a second check, but never rely on it as the only one.
