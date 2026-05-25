# IPA Build & Distribution

This repository contains automated workflows to build and distribute iOS IPA files online.

## Features

- ✅ Automated IPA builds using GitHub Actions
- ✅ Online distribution via GitHub Releases
- ✅ Build artifacts stored for easy access
- ✅ Customizable build configurations

## Quick Start

1. **Add your iOS project** to this repository
2. **Configure** the build workflow (`.github/workflows/build.yml`)
3. **Trigger** a build manually or via push events
4. **Download** your IPA from Releases or Artifacts

## Setup Instructions

### Prerequisites
- macOS runner (for iOS builds)
- Xcode project or Xcode workspace
- Apple Developer Certificate & Provisioning Profile (for production builds)

### Configuration

See `.github/workflows/build.yml` for build configuration options.

## Distribution Methods

### 1. GitHub Releases
IPA files are automatically uploaded to GitHub Releases for easy downloading.

### 2. GitHub Actions Artifacts
Build artifacts are stored for 90 days (configurable).

### 3. Custom Hosting
You can configure additional hosting (S3, Firebase, etc.) in the workflow.

## Building Locally

```bash
xcodebuild -scheme YourScheme -configuration Release -derivedDataPath build archive -archivePath build/YourApp.xcarchive
xcodebuild -exportArchive -archivePath build/YourApp.xcarchive -exportOptionsPlist exportOptions.plist -exportPath build/ipa
```

## License

[Add your license here]
