// fsn-icons-sync
//
// Pulls the latest SVG icons from upstream sources and copies them into
// the local icon set directories.
//
// Uses git sparse-checkout with --depth=1 to fetch only SVG files.
// No git history, no PNGs, no WebP variants — SVGs only.
//
// Usage:
//   fsn-icons-sync                     → sync all sets
//   fsn-icons-sync --set homarrlabs    → sync only homarrlabs
//   fsn-icons-sync --icons-dir <path>  → use a custom icons root

use std::{
    fs,
    path::{Path, PathBuf},
    process::Command,
};

use clap::Parser;

const HOMARRLABS_URL: &str = "https://github.com/homarr-labs/dashboard-icons.git";
const WE10X_URL: &str = "https://github.com/yeyushengfan258/We10X-icon-theme.git";

/// FreeSynergy Icons Sync — pulls latest icons from upstream sources.
#[derive(Parser, Debug)]
#[command(name = "fsn-icons-sync", about = "Sync icon sets from upstream (SVG only)")]
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

    // Sparse clone: only fetch tree objects first, no blobs, no history
    println!("  Cloning (SVG only, depth=1)...");
    git(&["clone", "--filter=blob:none", "--sparse", "--depth=1",
          HOMARRLABS_URL,
          clone_path.to_str().unwrap()])?;

    // Restrict checkout to the svg/ directory only
    git_in(&clone_path, &["sparse-checkout", "set", "svg/"])?;
    git_in(&clone_path, &["checkout"])?;

    // Copy SVGs to target
    println!("  Clearing {}", target_dir.display());
    if target_dir.exists() {
        fs::remove_dir_all(&target_dir)?;
    }
    fs::create_dir_all(&target_dir)?;

    let svg_src = clone_path.join("svg");
    let mut count = 0usize;

    println!("  Copying SVGs...");
    for entry in fs::read_dir(&svg_src)? {
        let entry = entry?;
        let path = entry.path();
        if path.extension().and_then(|e| e.to_str()) == Some("svg") {
            let dest = target_dir.join(path.file_name().unwrap());
            fs::copy(&path, &dest)?;
            count += 1;
        }
    }

    println!("  ✓ homarrlabs: {count} SVGs copied");
    Ok(())
}

fn sync_we10x(icons_root: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let tmp_dir = tempfile::tempdir()?;
    let clone_path = tmp_dir.path().join("We10X-icon-theme");
    let target_dir = icons_root.join("We10X");

    // Sparse clone: only the scalable/ directory (SVGs), no history
    println!("  Cloning (SVG only, depth=1)...");
    git(&["clone", "--filter=blob:none", "--sparse", "--depth=1",
          WE10X_URL,
          clone_path.to_str().unwrap()])?;

    git_in(&clone_path, &["sparse-checkout", "set", "src/"])?;
    git_in(&clone_path, &["checkout"])?;

    // Copy all SVGs (recursively from subdirs) into target, preserving structure
    println!("  Clearing {}", target_dir.display());
    if target_dir.exists() {
        fs::remove_dir_all(&target_dir)?;
    }
    fs::create_dir_all(&target_dir)?;

    let svg_src = clone_path.join("src");
    let count = copy_svgs_recursive(&svg_src, &target_dir)?;

    println!("  ✓ we10x: {count} SVGs copied");
    Ok(())
}

/// Recursively walks `src_dir` and copies every *.svg into `dest_dir`,
/// preserving the subdirectory structure relative to `src_dir`.
fn copy_svgs_recursive(src_dir: &Path, dest_dir: &Path) -> Result<usize, Box<dyn std::error::Error>> {
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

fn git(args: &[&str]) -> Result<(), Box<dyn std::error::Error>> {
    let status = Command::new("git").args(args).status()?;
    if !status.success() {
        return Err(format!("git {} failed (exit {})", args.join(" "), status).into());
    }
    Ok(())
}

fn git_in(dir: &Path, args: &[&str]) -> Result<(), Box<dyn std::error::Error>> {
    let status = Command::new("git").current_dir(dir).args(args).status()?;
    if !status.success() {
        return Err(format!("git {} failed (exit {})", args.join(" "), status).into());
    }
    Ok(())
}
