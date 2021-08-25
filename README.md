# sysmenu

A configurable context menu maker. Uses ini configuration, formatted like Polybar. Similar to Polybar's `bar/` sections defining bars (*e.g.*, `[bar/top]` defines a new bar, top, opened with `polybar top`), sysmenu has `menu:` sections that are made up of components (*e.g.*, `[menu:system]` is `sysmenu system`).

## Configuration

### Global

The `global` section can be used to define general styling. this includes:

`background`: hex color
`foreground`: hex color
`highlight`: hex color, color on hover
`padding_x`: integer
`padding_y`: integer

### Menus

Menu sections must start with `menu:`. They can have any of the properties that `global` outlines, and have a few extra properties:

`x`: integer, the X coordinate to draw the top-left corner at
`y`: integer, the Y coordinate to draw the top-left corner at
`items`: space separated strings, the components to put in the menu.

### Components

All components have the following properties:

`text`: string, the text displayed on the component

`eval`: bool, whether or not the `text` string should be evaluated in the shell and its output displayed.
`font`: font name, the font to use for component text

#### Button

Buttons are defined in a section that starts with `button:`, and perform an action when clicked. They're also highlighted on hover. They have the following extra properties:

`command`: the shell command to run on click
`condition`: an evaluated expression that returns "true" if the button should be enabled.

#### Label

Labels just render text. They are defined by a section that starts with `label:`.

### Fonts

Fonts are defined in `font:` sections that MUST have the following properties:

`family`: string, the font family
`size`: integer, the font weight

To use a font, use the section name in the font field of a widget (*e.g.*, `[font:x]` is used via `font = x`).
