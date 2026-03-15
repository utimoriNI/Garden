
```yaml:dbfolder
name: new database
description: new description
columns:
  __file__:
    key: __file__
    id: __file__
    input: markdown
    label: File
    accessorKey: __file__
    isMetadata: true
    skipPersist: false
    isDragDisabled: false
    csvCandidate: true
    position: 2
    isHidden: false
    sortIndex: -1
    width: -59
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: true
      task_hide_completed: true
      footer_type: none
      persist_changes: false
      content_alignment: text-align-left
      wrap_content: false
  __tags__:
    key: __tags__
    id: __tags__
    input: metadata_tags
    label: File Tags
    accessorKey: __tags__
    isMetadata: true
    isDragDisabled: false
    skipPersist: false
    csvCandidate: false
    position: 3
    isHidden: true
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  cover:
    input: text
    accessorKey: cover
    key: cover
    id: cover
    label: cover
    position: 1
    skipPersist: false
    isHidden: false
    sortIndex: -1
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 0
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
  Status:
    input: tags
    accessorKey: Status
    key: Status
    id: Status
    label: Status
    position: 4
    skipPersist: false
    isHidden: false
    sortIndex: 1
    isSorted: true
    isSortedDesc: true
    options:
      - { label: "読みたい", value: "読みたい", color: "hsl(197, 95%, 90%)"}
      - { label: "読了", value: "読了", color: "hsl(87, 95%, 90%)"}
      - { label: "積読", value: "積読", color: "hsl(82, 95%, 90%)"}
      - { label: "中断", value: "中断", color: "hsl(345, 95%, 90%)"}
      - { label: "読んでる", value: "読んでる", color: "hsl(348, 95%, 90%)"}
      - { label: "[,読了]", value: "[,読了]", color: "hsl(162, 95%, 90%)"}
      - { label: "[,積読]", value: "[,積読]", color: "hsl(216, 95%, 90%)"}
      - { label: "[,読みたい]", value: "[,読みたい]", color: "hsl(80, 95%, 90%)"}
      - { label: "[,中断]", value: "[,中断]", color: "hsl(44, 95%, 90%)"}
      - { label: "[,読んでる]", value: "[,読んでる]", color: "hsl(0, 95%, 90%)"}
    config:
      enable_media_view: true
      link_alias_enabled: true
      media_width: 100
      media_height: 100
      isInline: false
      task_hide_completed: true
      footer_type: none
      persist_changes: false
config:
  remove_field_when_delete_column: false
  cell_size: compact
  sticky_first_column: false
  group_folder_column: 
  remove_empty_folders: false
  automatically_group_files: false
  hoist_files_with_empty_attributes: true
  show_metadata_created: false
  show_metadata_modified: false
  show_metadata_tasks: false
  show_metadata_inlinks: false
  show_metadata_outlinks: false
  show_metadata_tags: true
  source_data: tag
  source_form_result: "#📚Book"
  source_destination_path: /
  row_templates_folder: /
  current_row_template: 
  pagination_size: 70
  font_size: 16
  enable_js_formulas: false
  formula_folder_path: /
  inline_default: false
  inline_new_position: last_field
  date_format: yyyy-MM-dd
  datetime_format: "yyyy-MM-dd HH:mm:ss"
  metadata_date_format: "yyyy-MM-dd HH:mm:ss"
  enable_footer: false
  implementation: default
filters:
  enabled: true
  conditions:
      - field: Status
        operator: EQUAL
        value: "読みたい"
        type: tags
```