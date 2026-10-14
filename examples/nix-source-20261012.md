# Nix source inventory - 2026-10-12

Read-only inventory. No Nix or Home Manager configuration was modified, built, or switched. The settings file contents were not read.

## Search locations

Checked `~/.config/home-manager`, `~/.config/nix`, `~/Documents`, `~/Dev`, `~/dotfiles`, `~/.dotfiles`, and `/etc/nix-darwin` for configuration directories and Git repositories. The two `.config` paths, `~/Dev`, `~/dotfiles`, and `/etc/nix-darwin` are absent. `~/Documents` had no dotfiles or nix-config repository. `~/.dotfiles` is a symlink to `<home>/github/<github-user>/dotfiles`, which is the source repository found through the live symlink chain.

In that repository, searched the three `.nix` files (`home.nix`, `configuration.nix`, and `flake.nix`). Grepping nonempty lines from `home/AGENTS.md` found no literal text matches in `.nix` files. A path-reference search found the file mappings in `home.nix`.

## Paths

| Input path | Symlink chain | Final target | Editable source and search evidence | Git repository | Apply guidance |
| --- | --- | --- | --- | --- | --- |
| `~/.claude/CLAUDE.md` | `<home>/.claude/CLAUDE.md` -> `/nix/store/kkpf1rkfak86q2vyxjchddh9nzg8xzqd-home-manager-files/.claude/CLAUDE.md` -> `/nix/store/zrbs4h9dw82p2dq0id6vj15gj8jwsncl-hm_AGENTS.md` -> `<home>/.dotfiles/home/AGENTS.md` -> `<home>/github/<github-user>/dotfiles/home/AGENTS.md` | `<home>/github/<github-user>/dotfiles/home/AGENTS.md` | Same file is editable source. `home.nix:87-88` maps it with `mkOutOfStoreSymlink`. Confirmed with `ls -l`, `readlink -f`, and the `.nix` reference search above. | Yes. Root: `<home>/github/<github-user>/dotfiles`. Shared status below. | No command for editing this symlinked source. README says: “The files under `home/` are the real files - editing them here is editing your live config, no rebuild needed to see the change in your editor.” |
| `~/.claude/settings.json` | `<home>/.claude/settings.json` -> `/nix/store/kkpf1rkfak86q2vyxjchddh9nzg8xzqd-home-manager-files/.claude/settings.json` -> `/nix/store/xdpd2sqd04ha1b07zc6qqd8kskkf164f-hm_settings.json` -> `<home>/.dotfiles/home/.claude/settings.json` -> `<home>/github/<github-user>/dotfiles/home/.claude/settings.json` | `<home>/github/<github-user>/dotfiles/home/.claude/settings.json` | Same file is editable source. `home.nix:74-75` maps it with `mkOutOfStoreSymlink`. Confirmed with `ls -l`, `readlink -f`, and the `.nix` reference search above. | Yes. Root: `<home>/github/<github-user>/dotfiles`. Shared status below. | No command for editing this symlinked source. README says: “The files under `home/` are the real files - editing them here is editing your live config, no rebuild needed to see the change in your editor.” |
| `~/.codex/AGENTS.md` | `<home>/.codex/AGENTS.md` -> `/nix/store/kkpf1rkfak86q2vyxjchddh9nzg8xzqd-home-manager-files/.codex/AGENTS.md` -> `/nix/store/zrbs4h9dw82p2dq0id6vj15gj8jwsncl-hm_AGENTS.md` -> `<home>/.dotfiles/home/AGENTS.md` -> `<home>/github/<github-user>/dotfiles/home/AGENTS.md` | `<home>/github/<github-user>/dotfiles/home/AGENTS.md` | Same file is editable source. `home.nix:89-90` maps it with `mkOutOfStoreSymlink`. Confirmed with `ls -l`, `readlink -f`, and the `.nix` reference search above. | Yes. Root: `<home>/github/<github-user>/dotfiles`. Shared status below. | No command for editing this symlinked source. README says: “The files under `home/` are the real files - editing them here is editing your live config, no rebuild needed to see the change in your editor.” |

For changes to Nix wiring rather than these symlinked source files, README.md also says: “You only run `./rebuild.sh` when you change something that isn't just a symlinked file, like a package list or a system default.”

### `git status --short` of the shared source repository

```text
 M home.nix
 M home/.claude/settings.json
 M home/.config/wezterm/wezterm.lua
 M home/.pi/agent/settings.json
?? home/.config/herdr/.plugins.lock
?? home/.config/herdr/release-notes.json
```

`home/AGENTS.md` itself is not listed as modified. The status above was already present during this read-only inspection.
