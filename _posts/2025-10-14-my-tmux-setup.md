---
title: My Tmux setup
date: 2024-03-16T19:08:02+0100
lastmod: 2024-03-16T19:08:02+0100
draft: false
description: My Tmux setup
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
---

I have been using `tmux` for quite a while now. Despite the fact that, I sometimes felt weird because of all the other colleagues use VSCODE
I never thought of coming back to one of these fameous IDEs. I did not configure my tmux in crazy way however, I like taking the most of it.
Whenever I created a new window (Ctrl+A+c) I immediatelly named it accordingly (Ctrl+A+,). This approach worked quite well for me but I soon figured that
it was not consistent at all. When under time preassure, I often ended up with many unnamed windows e.g [~zsh]. I kept using these incorrectly named windows and soon after ... I could not figure out what is where.


I had a very specific solution to this problem thus, I had no idea how to implement it correctly and I simply did not pay enough attention to this.

At some point, I have said that it has been enough. Surprisengly I found a very solid solution for myself.

The general idea is thatall of my work git repositories are stored in `~/Documents/work/`.

Whenever I needed to create a new window and jump into a folder I used.

```
ff='cd ~/Documents/work/$(cd ~/Documents/work && ls -d */  | fzf)'
```

It worked as charm but I always had to do one additional step. This was renaming of a current window using (Ctrl+A+,). And this was my pain point. I wanted to come up with a name very fast and soon I ended up with very inconsistent naming convention. Not only naming convention was a problem. When switching among windows, I used famous (Ctrl+A+w) that give a user nice overview thus it requires either using arrows up/down to find a proper window (git repo) or hitting `/` and typing some string to match a target.


What is the solution then ?

My preference was that I would wish to:

- list through all of my git repos within `~/Documents/work/` folder
- based on results, open new tmux window for each folder
- give a window the appropriate name - name of a git repo
- split each window horizontally with 82:18 ratio so each window would automatically have a space for `Nvim` (editor) and terminal below it.

The hardest part for me was to understand how to use `tmux` commands: `new-window` and `new-session`.

How to start?

It is obvious that I had to start a new `tmux` session first.

```
# opens up a new tmux session and detaches off
tmux new-session -s "mac" -n work -d
```

Then I figured that I have to `enumerate` windows if I want to create them in already existing `tmux` session. Since this is `bash` - there is probably nothing easier than `$(ls -d */ | nl -s:)`. Now I got git repos in following format:

```
    ...
    52:terraform-xyz-test/
    53:terraform-xyz-abs/
    56:utilities/
    ...
```

The rest of the code does magic for me.


```bash
[arch:blog main()] cat  ~/.config/thelper.sh
#!/bin/bash

# opens up a new tmux session and detaches off
tmux new-session -s "mac" -n work -d

# find all of the folders and enumerate them
for i in  $(ls -d */ | nl -s:); do
  wdir=${i##*:}   # takes repo name without number
  DIR=${wdir%/*}  # removes trailing slash

  tmux new-window -t "mac:${i%:*}" -n "${DIR}" -c "${DIR}";
  tmux split-window -t "mac:${i%:*}" -v -c "#{pane_current_path}" -l '18%';
done

```


Another option to use this script is to create a function in `~/.zshrc` file.

```bash
function tmux-crowler()
{
  tmux new-session -s "mac" -n work -d

  tmux new-window -t "mac:2" -n "home" -c "${HOME}";
  tmux select-pane -t "mac:2" -U;

  for i in  $(ls -d ~/Documents/work/*/ | nl -v3 -s:); do
    wdir=${i##*:}
    DIR=${wdir%/*}
    tmux new-window -t "mac:${i%:*}" -n "${DIR}" -c "${DIR}";
    tmux split-window -t "mac:${i%:*}" -v -c "#{pane_current_path}" -l '14%';
    tmux select-pane -t "mac:${i%:*}" -U;
  done


}
```

Now what?

Despite the fact that my desired `tmux` goal came finally true, there was one additional, yet very important challenge.

How to swiftly switch/jump between the `tmux` windows? As already mentioned, a native shortcut (Ctrl+A+w) was rather slow for me.

It turns out that there is `tmux` plugin that using fzf and it works quite well.

```bash
bind-key / run-shell -b "~/.tmux/plugins/tmux-fzf/scripts/window.sh switch"
TMUX_FZF_PREVIEW=0
set -g @plugin 'sainnhe/tmux-fzf'
```

Well, whenever I need to switch between `tmux` windows smoothly, I simply hit (Ctrl+A+/) and `fzf` like search bar appears.

I also crafted my own `alias` but from some reason I prefer using (Ctrl+A+/) better.

Here is a simple alias that does the same job as `tmux` plugin.

```bash
alias tt='tmux list-windows | fzf | cut -d: -f1 | xargs tmux select-window -t'

```


