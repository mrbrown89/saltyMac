installomator_apps:
  swiftdialog:
    label: swiftdialog
    name: Dialog
    bundle_id: au.csiro.dialog
    search_paths:
      - /Library/Application Support/Dialog
    args:
      - BLOCKING_PROCESS_ACTION=ignore
      - NOTIFY=silent

  windowsapp:
    label: microsoftwindowsapp
    name: Windows App
    bundle_id: com.microsoft.rdc.macos
    args:
      - BLOCKING_PROCESS_ACTION=silent_fail
      - NOTIFY=silent
      - DEBUG=0

  apparency:
    label: apparency
    name: Apparency
    bundle_id: com.mothersruin.Apparency
    args:
      - BLOCKING_PROCESS_ACTION=silent_fail
      - NOTIFY=silent
      - DEBUG=0
