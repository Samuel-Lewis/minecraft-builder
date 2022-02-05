# Schematic Prep

- Schematics should always be NORTH/SOUTH, with slices of the schematic extending EAST
- WEST most slice is slice 0
- Every slice must be the same width
- ![Schematic rendering cords](./docs/render_cords.png)
- There should be a one block gap between each slice
- ![Schematic rendering cords](./docs/schematic_layout.png)
- Barrier blocks and all air block types are are ignored

# Resources

- [Minecraft Schematic File Format](https://minecraft.fandom.com/wiki/Schematic_file_format)
- [Isometric renderings](https://github.com/gliscowo/isometric-renders)

# Development

Areas for development

- Aliasing. Renders don't look very clean at the moment.
- Pixel alignment. Sometimes gaps can be seen between blocks. Unsure if this is dirty assets or floating point errors in positioning.
- Rendering streaming. Want to find a way to efficiently pipe to ffmpeg (or some video library) directly.
- Removal of blocks. If a block is removed in a slice (eg, temp blocks in building), they currently do not animate out
- Asset generation. Asset generation is messy and requires lots of manual work. Maybe consider Fabric [game-test](https://github.com/FabricMC/fabric/tree/1.18/fabric-gametest-api-v1) API for generating renders?
- Code quality. Code is not very "pythonic", is missing some types (or type assertions) and has some wobbly naming. I'm pretty new to industry quality Python, so learning as I go.

## Python Virtual Env

### Unix (Linux/macOS)

- Enter env: `source .env/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Exit env: `deactivate`

### Windows

- Use _Command Prompt_ instead of _Windows Powershell_ (I can't work out why, but that's how it works for me)
- Enter env: `.\.env\Scripts\activate`
- Exit env: `deactivate`
