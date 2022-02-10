# Demo

![Demo](./docs/demo.gif)

Note: There are some artifacts in the demo (eg, bad transparency) that are not present in the actual production output. They're a sympton of the gif creation and optimisation process.

# Setup

## Schematics

- Schematics should always be NORTH/SOUTH, with the slices extending EAST
- Every slice of the schematic needs to be the same width
- Barrier blocks and all air block types are are ignored
  ![Schematic rendering cords](./docs/cords.png)
- The schematic border
  - All schematics must have the 1 wide border (on all axis), even if the schematic is only 1 slice
  - Include the border in your schematic
  - The gap between slices only needs to be 1 block wide
    ![Schematic rendering cords](./docs/slice_demo.png)

## Block renders

For block spawning and asset naming, just run the schematic through once and it will generate a `missing.txt` with the `/isorender` command and path/name of the asset. At the moment, this is quite a manual process (sorry), but we're looking into better solutions.

Rendering settings:

- `scale`: 304
- `rotation`: 315
- `angle`: 36 (isometric)
- `render height`: 0
- `lighting profile`: flat
- `animations`: false
- `render resolution`: 512
- `external renderer`: true

# Resources

- [Minecraft Schematic File Format](https://minecraft.fandom.com/wiki/Schematic_file_format)
- [Isometric renderings](https://github.com/gliscowo/isometric-renders)

# Development

Areas for development

- Aliasing. Renders don't look very clean at the moment.
- Asset generation. Asset generation is messy and requires lots of manual work. Maybe consider Fabric [game-test](https://github.com/FabricMC/fabric/tree/1.18/fabric-gametest-api-v1) API for generating renders?
- Code quality. Code is not very "pythonic", is missing some types (or type assertions) and has some wobbly naming. I'm pretty new to industry quality Python, so learning as I go.
- Entity rendering. Entities are rendered on the same layer as blocks, which will often conflict. Maybe need to introduce an entity layer.
- Pixel alignment. Sometimes gaps can be seen between blocks. Unsure if this is dirty assets or floating point errors in positioning.
- Removal of blocks. If a block is removed in a slice (eg, temp blocks in building), they currently do not animate out
- Rendering streaming. Want to find a way to efficiently pipe to ffmpeg (or some video library) directly.

## Python Virtual Env

### Unix (Linux/macOS)

- Enter env: `source .env/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Exit env: `deactivate`

### Windows

- Use _Command Prompt_ instead of _Windows Powershell_ (I can't work out why, but that's how it works for me)
- Enter env: `.\.env\Scripts\activate`
- Exit env: `deactivate`
