// fs-icons-sync
//
// Pulls the latest SVG icons from upstream sources and copies them into
// the local icon set directories.
//
// Uses gix (shallow clone, depth=1) to fetch only one commit worth of data.
// SVG filtering happens in Rust after checkout — no system git required.
//
// Usage:
//   fs-icons-sync                     → sync all sets
//   fs-icons-sync --set homarrlabs    → sync only homarrlabs
//   fs-icons-sync --icons-dir <path>  → use a custom icons root

use std::{
    fs,
    num::NonZeroU32,
    path::{Path, PathBuf},
};

use clap::Parser;

const HOMARRLABS_URL: &str = "https://github.com/homarr-labs/dashboard-icons.git";
const WE10X_URL: &str = "https://github.com/yeyushengfan258/We10X-icon-theme.git";

/// FreeSynergy Icons Sync — pulls latest icons from upstream sources.
#[derive(Parser, Debug)]
#[command(
    name = "fs-icons-sync",
    about = "Sync icon sets from upstream (SVG only)"
)]
struct Args {
    /// Sync only a specific set ID (e.g. "homarrlabs"). Syncs all if omitted.
    #[arg(long)]
    set: Option<String>,

    /// Root directory of the icons repo (defaults to current directory).
    #[arg(long)]
    icons_dir: Option<PathBuf>,
}

fn main() {
    let args = Args::parse();

    let icons_root = args
        .icons_dir
        .unwrap_or_else(|| std::env::current_dir().expect("Cannot determine current directory"));

    let sets_to_sync: Vec<&str> = match args.set.as_deref() {
        Some(s) => vec![s],
        None => vec!["homarrlabs", "we10x"],
    };

    for set_id in sets_to_sync {
        println!("→ Syncing set: {set_id}");
        if let Err(e) = sync_set(set_id, &icons_root) {
            eprintln!("✗ Failed to sync {set_id}: {e}");
            std::process::exit(1);
        }
    }

    println!("✓ All sets synced.");
}

fn sync_set(set_id: &str, icons_root: &Path) -> Result<(), Box<dyn std::error::Error>> {
    match set_id {
        "homarrlabs" => sync_homarrlabs(icons_root),
        "we10x" => sync_we10x(icons_root),
        other => Err(format!("Unknown set: {other}").into()),
    }
}

fn sync_homarrlabs(icons_root: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let tmp_dir = tempfile::tempdir()?;
    let clone_path = tmp_dir.path().join("dashboard-icons");
    let target_dir = icons_root.join("homarrlabs");

    println!("  Cloning (SVG only, depth=1)...");
    clone_shallow(HOMARRLABS_URL, &clone_path)?;

    println!("  Clearing {}", target_dir.display());
    if target_dir.exists() {
        fs::remove_dir_all(&target_dir)?;
    }
    fs::create_dir_all(&target_dir)?;

    // Copy only .svg files from the svg/ subdirectory
    let svg_src = clone_path.join("svg");
    let mut count = 0usize;

    println!("  Copying SVGs...");
    if svg_src.is_dir() {
        for entry in fs::read_dir(&svg_src)? {
            let entry = entry?;
            let path = entry.path();
            if path.extension().and_then(|e| e.to_str()) == Some("svg") {
                let dest = target_dir.join(path.file_name().unwrap());
                fs::copy(&path, &dest)?;
                count += 1;
            }
        }
    }

    println!("  ✓ homarrlabs: {count} SVGs copied");
    Ok(())
}

fn sync_we10x(icons_root: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let tmp_dir = tempfile::tempdir()?;
    let clone_path = tmp_dir.path().join("We10X-icon-theme");
    let target_dir = icons_root.join("we10x");

    println!("  Cloning (SVG only, depth=1)...");
    clone_shallow(WE10X_URL, &clone_path)?;

    println!("  Clearing {}", target_dir.display());
    if target_dir.exists() {
        fs::remove_dir_all(&target_dir)?;
    }
    fs::create_dir_all(&target_dir)?;

    // Copy all SVGs recursively from src/ subdirectory, preserving structure
    let svg_src = clone_path.join("src");
    let count = copy_svgs_recursive(&svg_src, &target_dir)?;

    println!("  ✓ we10x: {count} SVGs copied");
    Ok(())
}

/// Recursively walks `src_dir` and copies every *.svg into `dest_dir`,
/// preserving the subdirectory structure relative to `src_dir`.
fn copy_svgs_recursive(
    src_dir: &Path,
    dest_dir: &Path,
) -> Result<usize, Box<dyn std::error::Error>> {
    let mut count = 0usize;
    for entry in fs::read_dir(src_dir)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            let sub = dest_dir.join(path.file_name().unwrap());
            fs::create_dir_all(&sub)?;
            count += copy_svgs_recursive(&path, &sub)?;
        } else if path.extension().and_then(|e| e.to_str()) == Some("svg") {
            fs::copy(&path, dest_dir.join(path.file_name().unwrap()))?;
            count += 1;
        }
    }
    Ok(count)
}

/// Clones `url` into `target` with depth=1 (shallow) using gix — no system git required.
///
/// Note: sparse checkout is not used; SVG filtering happens in Rust after checkout.
/// This downloads slightly more data than the previous git sparse-checkout approach,
/// but eliminates the external `git` dependency entirely.
fn clone_shallow(url: &str, target: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let mut prepare = gix::clone::PrepareFetch::new(
        url,
        target,
        gix::create::Kind::WithWorktree,
        gix::create::Options::default(),
        gix::open::Options::isolated(),
    )?;

    prepare = prepare.with_shallow(gix::remote::fetch::Shallow::DepthAtRemote(
        NonZeroU32::new(1).unwrap(),
    ));

    let (mut checkout, _outcome) =
        prepare.fetch_then_checkout(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;

    checkout.main_worktree(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;

    Ok(())
}
