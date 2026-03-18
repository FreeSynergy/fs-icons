// fsn-icons-sync
//
// Pulls the latest SVG icons from upstream sources and copies them into
// the local icon set directories.
//
// Usage:
//   fsn-icons-sync                     → sync all sets
//   fsn-icons-sync --set homarrlabs    → sync only homarrlabs
//   fsn-icons-sync --icons-dir <path>  → use a custom icons root

use std::{
    fs,
    path::{Path, PathBuf},
};

use clap::Parser;

const HOMARRLABS_URL: &str = "https://github.com/homarr-labs/dashboard-icons.git";

/// FreeSynergy Icons Sync — pulls latest icons from upstream sources.
#[derive(Parser, Debug)]
#[command(name = "fsn-icons-sync", about = "Sync icon sets from upstream")]
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
        None => vec!["homarrlabs"],
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
        other => Err(format!("Unknown set: {other}").into()),
    }
}

fn sync_homarrlabs(icons_root: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let tmp_dir = tempfile::tempdir()?;
    let clone_path = tmp_dir.path().join("dashboard-icons");
    let target_dir = icons_root.join("homarrlabs");

    println!("  Cloning {HOMARRLABS_URL}...");
    clone_repo(HOMARRLABS_URL, &clone_path)?;

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

fn clone_repo(url: &str, target: &Path) -> Result<(), Box<dyn std::error::Error>> {
    let mut prepare = gix::clone::PrepareFetch::new(
        url,
        target,
        gix::create::Kind::WithWorktree,
        gix::create::Options::default(),
        gix::open::Options::isolated(),
    )?;
    prepare = prepare.with_remote_name("origin")?;

    let (mut checkout, _outcome) = prepare.fetch_then_checkout(
        gix::progress::Discard,
        &gix::interrupt::IS_INTERRUPTED,
    )?;

    let (_repo, _outcome) =
        checkout.main_worktree(gix::progress::Discard, &gix::interrupt::IS_INTERRUPTED)?;

    Ok(())
}
