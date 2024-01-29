# FileSorter

Simple file sorter, for moving file automatically; it use a configuration file to define multiple rule for a specific directory.

## Rules

| Type   | Arguments           |
| ------ | ------------------- |
| Move   | Filter              |
| Keep   | Filter              |
| Delete | Filter, Destination |
| Trash  | Filter              |

## First Run

Running the main file will create a file in the user directory ~, with a default config file.

## Configuration

```yaml
[
  {
    path: "/path1",
    enabled: true,
    rules: [{ type:"Move", filter: "**/*.*", to: "/path1/moved" }],
  },
  {
    path: "/path2",
    enabled: false,
    rules: [{ type:"Trash", filter: "*.ext" }],
  },
]
```
