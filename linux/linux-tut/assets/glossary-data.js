// Glossary data (generated from research/gloss-part*.json by research/build-glossary.py — edit those and rerun).
// Each entry: slug -> { name, short, def, also?, see? }
window.GLOSSARY = {
  "shell": {
    "name": "Shell",
    "short": "The program that reads the command lines you type (or a harness sends), works out what they mean, starts the programs they name, and reports the result.",
    "def": "A shell is an ordinary program whose job is to turn a line of text into running programs: it splits the line into words, expands variables and wildcards, finds the program named by the first word, starts it, waits, and records its <a href='pages/02-shell-and-commands.html'>exit status</a>. It exists so that people and scripts can drive the operating system without writing C. On Ubuntu the interactive shell is <code>bash</code>; <code>/bin/sh</code> is a smaller shell called <code>dash</code>, and Alpine has neither by default. An agent's bash tool is just a harness feeding strings to a shell inside the sandbox, so most of what looks odd in a transcript &mdash; quoting errors, a missing <code>PATH</code> entry, <code>command not found</code> &mdash; is shell behaviour, not model behaviour.",
    "also": "command-line interpreter, sh",
    "see": [
      "bash",
      "terminal",
      "command",
      "bash-tool",
      "posix"
    ]
  },
  "terminal": {
    "name": "Terminal",
    "short": "The window (or program) that displays text and sends your keystrokes to a shell; it shows characters, while the shell is what actually interprets commands.",
    "def": "A terminal is the program that draws text on your screen and passes keystrokes along &mdash; Terminal.app or iTerm on a Mac. It is not the thing that understands commands; that is the <a href='pages/02-shell-and-commands.html'>shell</a> running inside it. The split is historical (terminals were once physical devices wired to a computer) but it still matters: colours, line editing, and a program's decision to prompt or page all depend on whether it believes a terminal is attached. An agent in a sandbox usually has a shell with <em>no</em> terminal, which is why tools behave differently for it than they do when you try the same command by hand. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "terminal emulator, console",
    "see": [
      "shell",
      "tty",
      "tmux",
      "interactive-prompt"
    ]
  },
  "bash": {
    "name": "bash",
    "short": "The Bourne Again Shell: the default interactive shell on Ubuntu and Debian and the language most eval setup scripts and agent commands are written in.",
    "def": "<code>bash</code> is the shell you get by default on Ubuntu and Debian, and the dialect almost every benchmark's setup script assumes. It is a superset of the POSIX <code>sh</code> language, adding arrays, <code>[[ ]]</code> tests, and <code>set -o pipefail</code>. Three environments differ from that default and each bites: macOS uses <code>zsh</code> interactively and ships an old bash 3.2; Ubuntu's <code>/bin/sh</code> is <code>dash</code>, so a script run as <code>sh script.sh</code> loses the bash features; and Alpine images have no bash at all unless someone installs it. When an agent's command fails with <code>bash: not found</code> in an Alpine task image, that is an environment fact to record, not a reasoning error. Taught on <a href='pages/02-shell-and-commands.html'>page 2</a> and <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "Bourne Again Shell",
    "see": [
      "shell",
      "posix",
      "busybox",
      "shebang",
      "strict-mode"
    ]
  },
  "command": {
    "name": "Command",
    "short": "The first word of a shell line: the name of the program, builtin, function, or alias to run, with the remaining words passed to it as arguments.",
    "def": "A command line is a list of words; the first word names what to run and the rest are handed to it. That first word can resolve to four different things &mdash; an alias, a shell function, a <a href='pages/02-shell-and-commands.html'>builtin</a>, or an executable file found by searching the directories in <code>PATH</code> &mdash; and <code>type name</code> tells you which. Knowing this lets you derive the two most common transcript errors instead of memorising them: <code>command not found</code> (exit status 127) means the search came up empty, and <code>Permission denied</code> (126) means a file was found but is not executable. Both usually point at the task image, not at the agent.",
    "see": [
      "argument",
      "option-flag",
      "path-variable",
      "builtin",
      "exit-status"
    ]
  },
  "argument": {
    "name": "Argument",
    "short": "One of the words after the command name, passed to the program as a separate string; the shell decides where one argument ends and the next begins.",
    "def": "Arguments are the words that follow the command name. The shell splits the line into words <em>before</em> the program starts, and the program receives a finished list of strings &mdash; it never sees your spaces or quotes. That is why <code>rm my file.txt</code> tries to delete two files and why <a href='pages/06-shell-scripting.html'>quoting</a> exists: quotes are instructions to the shell about where word boundaries go. When a harness runs an agent's command, check whether it passes one string to <code>bash -c</code> (the shell splits it) or a pre-split list to <code>exec</code> (no shell involved, so no globs, pipes, or variables). The same text behaves differently under the two. See <a href='pages/02-shell-and-commands.html'>page 2</a>.",
    "also": "parameter, argv",
    "see": [
      "command",
      "option-flag",
      "quoting",
      "glob"
    ]
  },
  "option-flag": {
    "name": "Option (Flag)",
    "short": "An argument beginning with a dash, such as -l or --help, that changes how a command behaves rather than naming something for it to act on.",
    "def": "An option is just an argument that, by convention, starts with <code>-</code> (short, one letter, combinable: <code>ls -la</code>) or <code>--</code> (long: <code>--recursive</code>). Nothing in the kernel enforces this; each program parses its own arguments, which is why conventions vary (<code>find -name</code>, <code>tar xzf</code>). A bare <code>--</code> means &ldquo;end of options&rdquo;, so a filename beginning with a dash is not mistaken for one. The practical trap is that the same option can differ between GNU, BSD/macOS, and BusyBox versions of a tool &mdash; <code>sed -i</code> is the classic &mdash; so a command that works on your Mac can fail in the task image. See <a href='pages/02-shell-and-commands.html'>page 2</a> and <a href='appendices/e-macos-vs-linux.html'>Appendix E</a>.",
    "also": "flag, switch, option",
    "see": [
      "argument",
      "command",
      "man-page",
      "gnu-coreutils",
      "busybox"
    ]
  },
  "path-variable": {
    "name": "PATH",
    "short": "An environment variable holding a colon-separated list of directories that the shell searches, in order, to find the program a command name refers to.",
    "def": "<code>PATH</code> is how the shell turns a bare name like <code>python3</code> into a file like <code>/usr/bin/python3</code>: it tries each listed directory in order and runs the first match. In an <code>ubuntu:24.04</code> container it is <code>/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin</code>. Because it is an <a href='pages/11-environment-and-secrets.html'>environment variable</a>, it is inherited, and different ways of entering the same box can see different values &mdash; a login shell reads profile files that a harness's non-interactive <code>exec</code> never touches. That is the usual cause of &ldquo;it's installed but the agent gets <code>command not found</code>&rdquo;: the tool lives in a virtualenv or <code>~/.local/bin</code> that is on your PATH but not on the harness's. Taught on <a href='pages/02-shell-and-commands.html'>page 2</a>.",
    "also": "$PATH, search path",
    "see": [
      "command",
      "environment-variable",
      "absolute-path",
      "exit-status",
      "virtual-environment"
    ]
  },
  "absolute-path": {
    "name": "Absolute Path",
    "short": "A file location written out in full from the root directory, starting with a slash, so it means the same thing wherever you currently are.",
    "def": "An absolute path starts at <code>/</code> and names every directory on the way down: <code>/var/log/syslog</code>. Because it does not depend on the current <a href='pages/03-files-and-the-tree.html'>working directory</a>, it is the unambiguous form &mdash; the one to use in Dockerfiles, harness configuration, and scorer code. It is absolute only within one view of the filesystem, though: <code>/workspace/tests</code> inside a container and <code>/workspace/tests</code> on the host are different places unless a mount makes them the same. When a transcript shows an agent writing its answer to a path the scorer never looks at, the first thing to establish is which filesystem each side was resolving that path in.",
    "also": "full path",
    "see": [
      "relative-path",
      "root-directory",
      "working-directory",
      "mount-namespace"
    ]
  },
  "relative-path": {
    "name": "Relative Path",
    "short": "A file location written relative to the current working directory, with no leading slash; the same text points to different files from different directories.",
    "def": "A relative path has no leading <code>/</code>; the kernel resolves it starting from the process's current <a href='pages/03-files-and-the-tree.html'>working directory</a>. Two special names help: <code>.</code> is the current directory and <code>..</code> is its parent, so <code>../data/in.json</code> means &ldquo;up one, then into data&rdquo;. Relative paths are convenient to type and fragile in automation, because their meaning depends on hidden state. A typical eval failure: the harness runs each tool call in a fresh shell, the agent's earlier <code>cd repo</code> did not persist, and <code>pytest tests/</code> now reports <code>No such file or directory</code>. That looks like the agent getting lost; it is actually the harness resetting the directory.",
    "see": [
      "absolute-path",
      "working-directory",
      "home-directory"
    ]
  },
  "working-directory": {
    "name": "Working Directory",
    "short": "The directory a process is currently 'in', which is where its relative paths start; every process has its own, inherited from its parent.",
    "def": "Each process carries a current working directory, inherited from the process that started it; <code>pwd</code> prints it and <code>cd</code> changes it. It is per-process state, which explains why <code>cd</code> must be a shell <a href='pages/02-shell-and-commands.html'>builtin</a>: a separate <code>cd</code> program could only change its own directory and then exit. The same logic explains a harness behaviour that confuses agents &mdash; if every tool call starts a new shell, a <code>cd</code> in one call has no effect on the next. Harnesses and Docker therefore set it explicitly (<code>WORKDIR</code>, <code>docker exec -w</code>, a <code>cwd</code> parameter). When auditing a task, check what directory the agent's commands actually start in. See <a href='pages/03-files-and-the-tree.html'>page 3</a> and <a href='pages/25-how-harnesses-use-linux.html'>page 25</a>.",
    "also": "cwd, current directory, pwd",
    "see": [
      "relative-path",
      "absolute-path",
      "builtin",
      "bash-tool"
    ]
  },
  "home-directory": {
    "name": "Home Directory",
    "short": "A user's personal directory, usually /home/name (or /root for root), where their files and per-user configuration live; the shell abbreviates it as ~.",
    "def": "Every account in <code>/etc/passwd</code> names a home directory: <code>/home/alice</code> for ordinary users, <code>/root</code> for root. The shell expands <code>~</code> to it and sets <code>HOME</code>, and tools use it to find per-user configuration &mdash; <code>~/.bashrc</code>, <code>~/.ssh</code>, <code>~/.cache/pip</code>, <code>~/.gitconfig</code>. That makes home a quiet source of differences between runs: the same command behaves differently as a different user because a different set of <a href='pages/03-files-and-the-tree.html'>dotfiles</a> applies. It is also a place leftovers hide. If a task image was built by someone working interactively, <code>~/.bash_history</code> or a cached credential may still be there for the agent to read. Users are covered on <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "~, $HOME",
    "see": [
      "dotfile",
      "user",
      "passwd-file",
      "working-directory"
    ]
  },
  "exit-status": {
    "name": "Exit Status",
    "short": "The number from 0 to 255 a program hands back when it ends: 0 means success, anything else means failure, and the shell stores it in $?.",
    "def": "When a process ends it reports one small integer to its parent. Zero means success; any non-zero value means failure, and the program chooses what its own codes mean. The shell stores the last one in <code>$?</code> and uses it for <code>&amp;&amp;</code>, <code>||</code>, and <code>if</code>. A few values are conventions of the shell itself: 126 (found but not executable), 127 (command not found), and 128+<em>n</em> for death by signal <em>n</em>, so 137 is SIGKILL and 143 is SIGTERM. For evals this number is often the entire verdict: a scorer that runs the tests and checks the status is only as good as the chain that carries it, and a pipeline such as <code>pytest | tee log</code> reports <code>tee</code>'s status, not pytest's. See <a href='pages/10-signals-exit-codes.html'>page 10</a> and <a href='appendices/b-exit-codes-signals.html'>Appendix B</a>.",
    "also": "exit code, return code, $?",
    "see": [
      "signal",
      "sigkill",
      "timeout",
      "pipe",
      "strict-mode"
    ]
  },
  "stdin": {
    "name": "Standard Input (stdin)",
    "short": "File descriptor 0: the channel a program reads its input from, connected to the keyboard by default or to a file or pipe when redirected.",
    "def": "Standard input is the already-open channel, numbered 0, that a program reads from when it is not given a file. At an interactive prompt it is your keyboard; with <code>&lt; file</code> it is a file; after a <code>|</code> it is the previous program's output. The program cannot easily tell which, and that is the design: it lets small tools be chained. For sandboxes the important case is stdin connected to <em>nothing</em>. A harness that runs commands without attaching input gives the program an immediate end-of-file or a closed descriptor, so anything that expects a typed answer &mdash; a confirmation, a password, a REPL &mdash; either fails at once or hangs until the timeout. Taught on <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "standard input, fd 0",
    "see": [
      "stdout",
      "stderr",
      "file-descriptor",
      "interactive-prompt",
      "pipe"
    ]
  },
  "stdout": {
    "name": "Standard Output (stdout)",
    "short": "File descriptor 1: the channel a program writes its normal results to, shown on the terminal by default and the only stream a pipe carries.",
    "def": "Standard output is channel number 1, where a program writes its results. By default it goes to the terminal; <code>&gt; file</code> sends it to a file and <code>|</code> sends it to the next program. It is deliberately separate from <a href='pages/04-streams-pipes-redirection.html'>stderr</a> so that results can be piped onward while diagnostics still reach a human. Two consequences matter in eval work. A harness that records only stdout will log an empty string when a test runner crashes and prints its traceback to stderr. And many programs buffer stdout in blocks when it is not a terminal, so output from a process that is later killed may never appear, and interleaved stdout/stderr in a log may not be in the order events happened.",
    "also": "standard output, fd 1",
    "see": [
      "stderr",
      "stdin",
      "redirection",
      "pipe",
      "transcript"
    ]
  },
  "stderr": {
    "name": "Standard Error (stderr)",
    "short": "File descriptor 2: a second output channel reserved for error messages and diagnostics, kept separate so it does not mix into a program's real results.",
    "def": "Standard error is channel number 2. It exists so that a program's complaints do not contaminate its data: in <code>sort names.txt &gt; out.txt</code>, an error message should reach you, not end up as a line in <code>out.txt</code>. Pipes and <code>&gt;</code> touch only channel 1, so stderr passes straight through to the terminal unless you redirect it as well (<code>2&gt; err.log</code>, or <code>2&gt;&amp;1</code> to merge it into wherever stdout currently points). When a transcript shows a command that &ldquo;printed nothing&rdquo; yet clearly failed, ask which streams the harness captured. Missing stderr turns a loud crash into a silent one, and the grader then scores a logging gap as a model failure. Taught on <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "standard error, fd 2",
    "see": [
      "stdout",
      "file-descriptor",
      "redirection",
      "exit-status",
      "transcript"
    ]
  },
  "file-descriptor": {
    "name": "File Descriptor",
    "short": "A small integer a process uses to refer to something it has open: a file, a pipe, a socket, or a terminal. 0, 1 and 2 are stdin, stdout and stderr.",
    "def": "When a process opens something, the kernel hands back a small number and the process uses that number for every later read or write. Files, pipes, network sockets, and terminals all work this way, which is the practical meaning of &ldquo;everything is a file&rdquo;. Descriptors 0, 1, and 2 are open before the program starts and are inherited from the parent, so redirection is simply the shell re-pointing those numbers before launching the program. This model makes <code>2&gt;&amp;1</code> derivable: &ldquo;make 2 refer to whatever 1 refers to right now&rdquo;. You can inspect any process's descriptors under <code>/proc/PID/fd</code>, which is how you find where a hung agent command is really writing, or which deleted log file still holds disk space. See <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "fd, file handle",
    "see": [
      "stdin",
      "stdout",
      "stderr",
      "redirection",
      "everything-is-a-file"
    ]
  },
  "pipe": {
    "name": "Pipe",
    "short": "A one-way channel, written |, that connects one program's standard output directly to the next program's standard input so they run as a chain.",
    "def": "A pipe is a kernel buffer with a write end and a read end. <code>a | b</code> starts both programs at once, with <code>a</code>'s stdout attached to the write end and <code>b</code>'s stdin to the read end; data flows as it is produced and nothing is written to disk. Only stdout travels &mdash; stderr still goes to the terminal. The part that catches people is the <a href='pages/10-signals-exit-codes.html'>exit status</a>: by default a pipeline reports only the <em>last</em> command's status, so <code>false | true</code> succeeds. A verifier that runs <code>pytest | tee results.log</code> and checks <code>$?</code> will pass every submission. <code>set -o pipefail</code> in bash changes the rule so any failing stage fails the pipeline. Taught on <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "pipeline, |",
    "see": [
      "stdout",
      "stdin",
      "redirection",
      "strict-mode",
      "exit-status"
    ]
  },
  "redirection": {
    "name": "Redirection",
    "short": "Shell syntax that re-points a program's input or output channels at files, or at each other, before the program starts; the program itself never sees it.",
    "def": "Redirection is the shell rearranging a program's file descriptors before launching it. <code>&gt; f</code> points stdout at a file (truncating it first), <code>&gt;&gt; f</code> appends, <code>&lt; f</code> points stdin at a file, and <code>2&gt; f</code> does the same for stderr. <code>2&gt;&amp;1</code> means &ldquo;make descriptor 2 a copy of whatever 1 is <em>now</em>&rdquo;, which is why order matters: <code>cmd &gt; log 2&gt;&amp;1</code> captures both streams, while <code>cmd 2&gt;&amp;1 &gt; log</code> leaves errors on the terminal. The program itself never sees any of this syntax. Two eval-relevant traps: <code>&gt;</code> empties the target even if the command then fails, and <code>sudo cmd &gt; /root/file</code> fails because the redirect is performed by your unprivileged shell. See <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "I/O redirection",
    "see": [
      "file-descriptor",
      "stdout",
      "stderr",
      "dev-null",
      "here-document"
    ]
  },
  "here-document": {
    "name": "Here-Document",
    "short": "Shell syntax that feeds the following lines of a script to a command as its standard input, up to a chosen end marker, without needing a separate file.",
    "def": "A here-document lets you put a block of input text inline: everything between <code>&lt;&lt;EOF</code> and a line containing only <code>EOF</code> becomes the command's stdin. The delimiter word is arbitrary. One detail decides whether it works: if the delimiter is unquoted, the shell still expands <code>$variables</code> and <code>$(commands)</code> inside the block; writing <code>&lt;&lt;'EOF'</code> turns expansion off and passes the text literally. Agents use here-documents constantly, because <code>cat &gt; file.py &lt;&lt;'EOF'</code> is the simplest way to create a file through a bash tool. When a transcript shows a written file with mangled dollar signs or missing backslashes, an unquoted delimiter is the first thing to check. Taught on <a href='pages/04-streams-pipes-redirection.html'>page 4</a> and used in <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "heredoc",
    "see": [
      "stdin",
      "redirection",
      "quoting",
      "variable-expansion"
    ]
  },
  "glob": {
    "name": "Glob",
    "short": "A wildcard pattern such as *.txt that the shell replaces with the list of matching filenames before the command ever runs.",
    "def": "Globbing is filename matching done by the shell: <code>*</code> matches any run of characters, <code>?</code> one character, <code>[abc]</code> one of a set. The shell expands the pattern into a sorted list of existing names and passes those as separate arguments, so <code>ls</code> never sees the asterisk. Three derived consequences: if nothing matches, bash passes the pattern through literally and you get an error about a file called <code>*.log</code>; <code>*</code> skips names beginning with a dot, so <code>cp * backup/</code> silently omits <code>.env</code> and <code>.git</code>; and quoting a pattern stops expansion, which is what you want when the pattern is meant for <code>find -name</code> or <code>grep</code>. Globs are not <a href='appendices/d-regex.html'>regular expressions</a> &mdash; <code>*</code> means something different in each. See <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "wildcard, pathname expansion",
    "see": [
      "regex",
      "quoting",
      "dotfile",
      "argument"
    ]
  },
  "quoting": {
    "name": "Quoting",
    "short": "Using single quotes, double quotes, or backslashes to tell the shell which characters to treat literally and where one argument ends and the next begins.",
    "def": "The shell gives meaning to spaces, <code>$</code>, <code>*</code>, <code>|</code>, <code>&gt;</code>, and more. Quoting switches that meaning off. Single quotes make everything literal. Double quotes keep the text as one word but still expand <code>$var</code> and <code>$(cmd)</code>. A backslash protects one character. The rule that prevents most script bugs follows directly: write <code>\"$file\"</code>, not <code>$file</code>, because an unquoted expansion is re-split on spaces and re-globbed, so a filename with a space becomes two arguments. Quoting gets harder with every layer a command passes through &mdash; JSON tool call, Python harness, <code>docker exec</code>, <code>bash -c</code> &mdash; and each layer strips one level. Mangled quotes in a transcript are as often the harness's fault as the model's. See <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "escaping",
    "see": [
      "variable-expansion",
      "glob",
      "argument",
      "here-document",
      "shellcheck"
    ]
  },
  "variable-expansion": {
    "name": "Variable Expansion",
    "short": "The shell replacing $NAME or ${NAME} in a command line with the variable's current value before the command runs.",
    "def": "Before running a line, the shell substitutes each <code>$NAME</code> with that variable's value; the program only ever sees the result. An unset variable expands to the empty string without complaint, which is how <code>rm -rf \"$BUILD_DIR/\"</code> becomes <code>rm -rf /</code> in a script where the variable was misspelled &mdash; and why <code>set -u</code> exists. Braces mark where the name ends (<code>${name}_v2</code>) and enable defaults (<code>${PORT:-8080}</code>). Expansion happens in whichever shell reads the text first. That matters when you drive a sandbox from outside: in <code>docker exec box bash -c \"echo $HOME\"</code>, the double quotes let your <em>host</em> shell expand <code>$HOME</code> before the container ever sees it. Taught on <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "parameter expansion, $VAR",
    "see": [
      "quoting",
      "environment-variable",
      "command-substitution",
      "strict-mode"
    ]
  },
  "command-substitution": {
    "name": "Command Substitution",
    "short": "The syntax $(command), which runs a command and inserts its standard output into the surrounding command line as text.",
    "def": "<code>$(cmd)</code> runs <code>cmd</code> in a subshell, captures its stdout, strips trailing newlines, and pastes the text in place: <code>today=$(date +%F)</code>. The older backtick form does the same but nests badly. Two properties are worth deriving. Only stdout is captured, so an error message from the inner command still goes to the terminal and the variable quietly ends up empty. And the result is subject to word splitting unless the whole thing is double-quoted: <code>\"$(cat file)\"</code>. In a scorer script, the pattern <code>result=$(run_tests)</code> followed by a string comparison will happily compare against an empty string if the test runner crashed, so check the exit status as well as the text. See <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "$(...), backticks",
    "see": [
      "variable-expansion",
      "quoting",
      "stdout",
      "exit-status"
    ]
  },
  "shebang": {
    "name": "Shebang",
    "short": "The first line of a script, starting with #!, that names the interpreter the kernel should run the file with, such as #!/bin/bash.",
    "def": "When you execute a file, the kernel looks at its first two bytes. If they are <code>#!</code>, it runs the program named on the rest of that line and passes the script's path as an argument, so <code>#!/bin/bash</code> means &ldquo;run this with bash&rdquo;. It is what lets a text file behave like a program once it also has execute permission. The shebang is a hard-coded path into the image, so it breaks across distributions: a script starting <code>#!/bin/bash</code> fails on Alpine with a confusing <code>not found</code> error that refers to the missing interpreter, not the script. <code>#!/usr/bin/env python3</code> searches <code>PATH</code> instead. Files saved with Windows line endings break it too, since the kernel looks for an interpreter whose name ends in a carriage return. See <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "hashbang, #!",
    "see": [
      "script",
      "bash",
      "permission-bits",
      "path-variable",
      "alpine"
    ]
  },
  "script": {
    "name": "Script",
    "short": "A text file of commands that an interpreter such as bash or Python runs from top to bottom, used to automate a sequence you would otherwise type by hand.",
    "def": "A shell script is the same language you type at the prompt, saved in a file. Eval environments are held together by them: the image's entrypoint, the task's setup script, the <code>run-tests.sh</code> a verifier calls. The default behaviour of bash is what makes them risky &mdash; a failing line does not stop the script, the script's exit status is just that of its last command, and unset variables expand to nothing. A setup script can therefore fail halfway, print an error nobody reads, exit 0, and leave a broken environment that every subsequent rollout is scored in. This course's rule is to keep shell scripts under about thirty lines, start them with strict mode, run them through ShellCheck, and move to Python beyond that. Taught on <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "shell script",
    "see": [
      "shebang",
      "strict-mode",
      "shellcheck",
      "exit-status",
      "entrypoint"
    ]
  },
  "strict-mode": {
    "name": "Strict Mode",
    "short": "The informal name for starting a bash script with set -euo pipefail so that it stops on errors, on unset variables, and on failures inside pipelines.",
    "def": "By default bash keeps going after a command fails. <code>set -euo pipefail</code> changes three defaults: <code>-e</code> exits when a command returns non-zero, <code>-u</code> treats an unset variable as an error rather than an empty string, and <code>-o pipefail</code> makes a pipeline fail if any stage fails, not just the last. Together they turn silent partial failure into a loud early exit, which is what you want from a task setup or scoring script. It is not a guarantee: <code>-e</code> is ignored for commands tested by <code>if</code>, <code>&amp;&amp;</code>, or <code>||</code>, and it makes <code>grep</code> finding no match (status 1) fatal unless you handle it. <code>pipefail</code> is a bash feature; do not assume it under a plain <code>sh</code>. See <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "also": "set -euo pipefail, unofficial bash strict mode",
    "see": [
      "script",
      "exit-status",
      "pipe",
      "shellcheck",
      "bash"
    ]
  },
  "shellcheck": {
    "name": "ShellCheck",
    "short": "A static analysis tool for shell scripts that flags common bugs, such as unquoted variables, before the script is ever run.",
    "def": "ShellCheck reads a shell script without executing it and reports likely mistakes, each with a code (<code>SC2086</code> is the famous one: an unquoted variable that will be split and globbed) and a wiki page explaining the reasoning. It exists because the shell language fails quietly: the bugs it finds are mostly ones that work on the author's test input and break on a filename with a space. For an evals engineer it is a cheap audit step. Running it over a benchmark's setup, entrypoint, and test-runner scripts takes seconds and regularly turns up the kind of defect that makes a task flaky or lets a failing test run report success. It is not installed by default; on Ubuntu it is the <code>shellcheck</code> package. Taught on <a href='pages/06-shell-scripting.html'>page 6</a>.",
    "see": [
      "script",
      "strict-mode",
      "quoting",
      "flaky-test"
    ]
  },
  "regex": {
    "name": "Regular Expression",
    "short": "A compact pattern language for describing text, such as ^ERROR.*timeout$, used by grep, sed, awk, and most programming languages to search and match strings.",
    "def": "A regular expression describes a set of strings: literal characters match themselves, <code>.</code> matches any character, <code>*</code> repeats the previous item, <code>[0-9]</code> is a character class, and <code>^</code> and <code>$</code> anchor to the start and end of a line. Tools disagree on dialect. Plain <code>grep</code> uses &ldquo;basic&rdquo; syntax in which <code>+</code>, <code>?</code>, <code>|</code>, and <code>()</code> need backslashes; <code>grep -E</code> uses &ldquo;extended&rdquo; syntax where they do not; and Python-style shorthands such as <code>\\d</code> are not part of either. Regexes are not <a href='pages/06-shell-scripting.html'>globs</a>. Many scorers are a regex over model output, so an unanchored or overly greedy pattern is a grading bug: it can accept an answer that merely contains the right string. See <a href='appendices/d-regex.html'>Appendix D</a> and <a href='pages/05-text-fu.html'>page 5</a>.",
    "also": "regexp, pattern",
    "see": [
      "grep",
      "sed",
      "awk",
      "glob",
      "scorer"
    ]
  },
  "grep": {
    "name": "grep",
    "short": "A command that prints the lines of its input that match a pattern; the standard tool for finding a needle in logs, code, or transcripts.",
    "def": "<code>grep PATTERN file</code> prints each line matching a regular expression. The options worth knowing: <code>-i</code> ignore case, <code>-v</code> invert, <code>-r</code> search a directory tree, <code>-n</code> show line numbers, <code>-c</code> count, <code>-E</code> extended regex, and <code>-F</code> treat the pattern as a fixed string. Its exit status carries meaning: 0 if something matched, 1 if nothing did, 2 on a real error. That makes it usable in <code>if</code> statements, and it also means a no-match <code>grep</code> will abort a script running under <code>set -e</code>. In eval work it is the first tool for triage at scale &mdash; counting how many of a thousand transcripts contain <code>command not found</code> or <code>Killed</code> tells you whether a failure is the model's or the environment's. Taught on <a href='pages/05-text-fu.html'>page 5</a>.",
    "see": [
      "regex",
      "sed",
      "awk",
      "exit-status",
      "error-analysis"
    ]
  },
  "sed": {
    "name": "sed",
    "short": "A stream editor: it reads text line by line, applies editing commands such as find-and-replace, and writes the result, without opening an interactive editor.",
    "def": "<code>sed</code> applies an editing script to each line of its input. Nearly all real use is two commands: substitution, <code>sed 's/old/new/g'</code>, and printing a range, <code>sed -n '10,20p' file</code>. By default it writes to stdout and leaves the file untouched; <code>-i</code> edits in place. Agents lean on it heavily because a bash tool has no interactive editor, so many code changes in a trajectory are <code>sed -i</code> one-liners &mdash; and a pattern that silently matches nothing still exits 0, leaving the agent believing it made an edit it did not. <code>-i</code> is also the best-known GNU/BSD incompatibility: on macOS it requires a backup-suffix argument (<code>sed -i ''</code>), so commands copied between your Mac and the sandbox break. See <a href='pages/05-text-fu.html'>page 5</a> and <a href='appendices/e-macos-vs-linux.html'>Appendix E</a>.",
    "also": "stream editor",
    "see": [
      "regex",
      "grep",
      "awk",
      "gnu-coreutils"
    ]
  },
  "awk": {
    "name": "awk",
    "short": "A small language for processing text arranged in columns: it splits each line into fields and lets you filter, print, and total them in one line.",
    "def": "<code>awk</code> reads input a line at a time, splits each line into fields (<code>$1</code>, <code>$2</code>, &hellip;, split on whitespace unless you set <code>-F</code>), and runs <code>pattern { action }</code> rules against it. That makes it the right tool whenever data is in columns: <code>awk '{print $1}'</code> to pull a column, <code>awk '$3 &gt; 100'</code> to filter on one, <code>awk '{s += $2} END {print s}'</code> to sum one. It fills the gap between <code>grep</code>, which cannot see columns, and writing a Python script. Typical eval use: totalling per-task durations from a harness log, or extracting the PID column from <code>ps</code> output. For JSON, use <code>jq</code> instead; awk does not understand nested structure. Taught on <a href='pages/05-text-fu.html'>page 5</a>.",
    "see": [
      "grep",
      "sed",
      "jq",
      "regex"
    ]
  },
  "jq": {
    "name": "jq",
    "short": "A command-line tool for reading, filtering, and reshaping JSON, doing for structured data what grep, sed, and awk do for plain lines of text.",
    "def": "<code>jq</code> takes a filter expression and applies it to JSON input: <code>jq '.score'</code> extracts a field, <code>jq '.messages[].role'</code> walks an array, <code>select(.status == \"error\")</code> filters, and <code>-r</code> prints raw strings without quotes. It exists because line-oriented tools break on JSON &mdash; a value can contain spaces, newlines, or escaped quotes, and <code>grep</code> has no idea where a field ends. Eval logs, Docker's <code>inspect</code> output, and most harness results are JSON or JSONL, so <code>jq</code> is how you answer questions like &ldquo;which samples hit the timeout?&rdquo; from a shell. It is not in the base <code>ubuntu:24.04</code> image; install the <code>jq</code> package. Taught on <a href='pages/05-text-fu.html'>page 5</a>.",
    "see": [
      "jsonl",
      "awk",
      "grep",
      "transcript"
    ]
  },
  "jsonl": {
    "name": "JSONL",
    "short": "JSON Lines: a text format with one complete JSON object per line, widely used for eval datasets, model transcripts, and logs.",
    "def": "A JSONL file holds one self-contained JSON value per line. The format exists because ordinary JSON is awkward for logs: a single top-level array must be read in full and is invalid until the closing bracket is written. With one record per line you can append safely, stream a file larger than memory, and use line tools &mdash; <code>wc -l</code> counts records, <code>head -1</code> shows the first, <code>split</code> shards the file &mdash; then hand each line to <a href='pages/05-text-fu.html'>jq</a>. The constraint is that a record may not contain a literal newline; newlines inside strings must be escaped as <code>\\n</code>. A run that crashed mid-write typically leaves a truncated last line, so a parse error on the final record of a results file points at the harness dying, not at bad data.",
    "also": "JSON Lines, NDJSON",
    "see": [
      "jq",
      "transcript",
      "trajectory",
      "grep"
    ]
  },
  "xargs": {
    "name": "xargs",
    "short": "A command that reads items from standard input and runs another command with those items as arguments, bridging pipes and programs that expect arguments.",
    "def": "Pipes deliver data on stdin, but many commands (<code>rm</code>, <code>cp</code>, <code>docker rm</code>) take their targets as arguments. <code>xargs</code> converts one into the other: <code>docker ps -aq | xargs docker rm</code>. By default it splits input on whitespace and treats quotes specially, so a filename with a space becomes two arguments. The safe pairing is <code>find &hellip; -print0 | xargs -0 &hellip;</code>, which separates names with a NUL byte that cannot occur in a path. <code>-n 1</code> runs the command once per item and <code>-P 4</code> runs four at a time, a quick way to parallelise a batch job over transcripts. With GNU xargs, empty input still runs the command once unless you pass <code>-r</code>. Taught on <a href='pages/05-text-fu.html'>page 5</a>.",
    "see": [
      "pipe",
      "argument",
      "stdin",
      "quoting"
    ]
  },
  "man-page": {
    "name": "Man Page",
    "short": "The reference manual entry for a command, file format, or system call, installed on the system and read with the man command.",
    "def": "<code>man ls</code> shows the manual for <code>ls</code>. Pages are grouped into numbered sections &mdash; 1 for commands, 2 for system calls, 5 for file formats, 7 for overviews, 8 for administration &mdash; which is what the number in a citation such as <code>signal(7)</code> means, and why <code>man 5 passwd</code> differs from <code>man passwd</code>. They are reference, not tutorial: read the synopsis, then search with <code>/</code>. Minimal container images strip them to save space; in <code>ubuntu:24.04</code> the <code>man</code> command is a stub that tells you so, which makes <code>cmd --help</code> and the online copies at man7.org the practical fallback. A man page documents the version installed <em>there</em>, which is the one that matters when macOS and the sandbox disagree. See <a href='appendices/f-getting-help.html'>Appendix F</a>.",
    "also": "manual page, man",
    "see": [
      "option-flag",
      "gnu-coreutils",
      "pager",
      "system-call"
    ]
  },
  "builtin": {
    "name": "Shell Builtin",
    "short": "A command implemented inside the shell itself rather than as a separate program, such as cd, export, or exit, because it must change the shell's own state.",
    "def": "Most commands are executable files the shell starts as child processes. A few cannot work that way, because a child cannot alter its parent: <code>cd</code> must change the shell's own working directory, <code>export</code> its own variables, <code>exit</code> must end it, <code>ulimit</code> must set its own limits. These are builtins. Others (<code>echo</code>, <code>test</code>, <code>kill</code>) are built in for speed and also exist as files. <code>type cd</code> reports &ldquo;cd is a shell builtin&rdquo;. The distinction explains several puzzles: <code>sudo cd /root</code> fails because there is no <code>cd</code> program for sudo to run; builtins are documented in <code>help cd</code>, not <code>man cd</code>; and a harness that executes a command list directly, with no shell, cannot run a builtin at all. Taught on <a href='pages/02-shell-and-commands.html'>page 2</a>.",
    "also": "built-in command",
    "see": [
      "command",
      "shell",
      "working-directory",
      "alias",
      "fork-exec"
    ]
  },
  "alias": {
    "name": "Alias",
    "short": "A shell shortcut that replaces one command word with another string, such as ll for ls -alF, defined per shell session and usually set in ~/.bashrc.",
    "def": "An alias is a text substitution the shell applies to the first word of a command: after <code>alias ll='ls -alF'</code>, typing <code>ll</code> runs the longer form. Ubuntu's default <code>~/.bashrc</code> defines <code>ll</code> and makes <code>ls</code> coloured this way. Aliases live only in the shell that defined them, and bash does not expand them at all in non-interactive shells &mdash; which is exactly the kind of shell a harness uses. So <code>bash -c ll</code> inside the same container returns <code>ll: command not found</code> with status 127. When an agent tries a command that works in every tutorial and the sandbox says it does not exist, check with <code>type</code> whether it was ever a real program. Keep aliases out of scripts; use functions or the full command. Taught on <a href='pages/02-shell-and-commands.html'>page 2</a>.",
    "see": [
      "command",
      "builtin",
      "dotfile",
      "bash-tool"
    ]
  },
  "tty": {
    "name": "TTY",
    "short": "A terminal device: the kernel object that connects a program to an interactive screen and keyboard. Programs check for one to decide whether a human is present.",
    "def": "TTY is short for teletypewriter; today it means a terminal device, usually a software pseudo-terminal (pty) created by your terminal app, <code>ssh</code>, <code>tmux</code>, or <code>docker run -t</code>. A program can ask whether its stdin or stdout is a TTY, and many change behaviour on the answer: with one, they use colour, progress bars, pagers, and prompts; without one, they print plain text and buffer output in blocks. The <code>tty</code> command prints the device name or <code>not a tty</code>. Most harnesses run agent commands with no TTY, so the agent sees different behaviour from what you see when you <code>docker exec -it</code> into the same box to reproduce a failure. Reproduce without <code>-t</code> first. See <a href='pages/27-reading-terminal-transcripts.html'>page 27</a> and <a href='pages/25-how-harnesses-use-linux.html'>page 25</a>.",
    "also": "pseudo-terminal, pty, terminal device",
    "see": [
      "terminal",
      "interactive-prompt",
      "pager",
      "tmux",
      "job-control"
    ]
  },
  "pager": {
    "name": "Pager",
    "short": "A program such as less that shows long output one screen at a time and waits for keypresses; convenient for people, a classic way for an agent to hang.",
    "def": "A pager takes output that is longer than the screen and lets you scroll through it; <code>less</code> is the usual one, and you leave it with <kbd>q</kbd>. Tools such as <code>git log</code>, <code>man</code>, <code>journalctl</code>, and <code>systemctl</code> start one automatically when their output is a terminal. For an agent driven through a terminal session, the pager sits waiting for a keypress the agent does not know it needs to send, and the command burns the task's time budget until the timeout fires. Defences belong in the environment: set <code>PAGER=cat</code> and <code>GIT_PAGER=cat</code>, or use <code>git --no-pager</code> and <code>--no-pager</code> for the systemd tools. A transcript ending in <code>:</code> or <code>(END)</code> is the signature. See <a href='pages/27-reading-terminal-transcripts.html'>page 27</a>.",
    "also": "less, more",
    "see": [
      "tty",
      "interactive-prompt",
      "timeout",
      "environment-variable",
      "man-page"
    ]
  },
  "interactive-prompt": {
    "name": "Interactive Prompt",
    "short": "A point where a program stops and waits for a person to type an answer, such as a yes/no confirmation or a password; in automation it causes hangs.",
    "def": "Many tools pause to ask a question: <code>apt-get install</code> asks &ldquo;Do you want to continue? [Y/n]&rdquo;, package configuration asks for a time zone, <code>ssh</code> asks whether to trust a new host key, <code>rm -i</code> asks before each file. With a person at a terminal that is a safety feature. In a sandbox there is nobody to answer, so the command either aborts when it reads end-of-file or waits until the harness's timeout kills it &mdash; and the transcript shows a run that &ldquo;did nothing&rdquo; for ten minutes. Each tool has a non-interactive switch: <code>-y</code> and <code>DEBIAN_FRONTEND=noninteractive</code> for apt, <code>--yes</code>, <code>--batch</code>, <code>-f</code> elsewhere. When classifying failures, count prompt hangs separately: they measure the environment and the agent's tool habits, not task ability. See <a href='pages/27-reading-terminal-transcripts.html'>page 27</a>.",
    "see": [
      "stdin",
      "tty",
      "pager",
      "timeout",
      "infrastructure-failure"
    ]
  },
  "tmux": {
    "name": "tmux",
    "short": "A terminal multiplexer: it runs shell sessions on the server that keep going after you disconnect and can be driven by other programs as well as people.",
    "def": "<code>tmux</code> starts a server process that owns one or more terminal sessions. You attach to a session to see and type into it, detach to leave it running, and reattach later &mdash; useful over SSH, where a dropped connection would otherwise kill your long-running job. It can also be scripted: <code>tmux send-keys</code> types into a session and <code>tmux capture-pane</code> reads the screen back. That is why some agent harnesses, Terminal-Bench among them, give the model a tmux session rather than a run-one-command function: the agent gets a real terminal with a TTY, so interactive programs, editors, and long-lived processes work. The cost is that the harness sees screen contents instead of separate stdout, stderr, and exit status, and must work out for itself when a command has finished. See <a href='pages/25-how-harnesses-use-linux.html'>page 25</a>.",
    "also": "terminal multiplexer",
    "see": [
      "tty",
      "terminal",
      "terminal-bench",
      "bash-tool",
      "sighup"
    ]
  },
  "ssh": {
    "name": "SSH",
    "short": "Secure Shell: the standard encrypted protocol and command for logging in to, and running commands on, a remote Linux machine over the network.",
    "def": "<code>ssh user@host</code> opens an encrypted connection to the SSH server on the remote machine (TCP port 22 by default) and gives you a shell there; <code>ssh user@host 'cmd'</code> runs one command and returns its exit status. Authentication is normally by key pair: the private key stays on your machine, the public key is listed in the server's <code>~/.ssh/authorized_keys</code>. It is how you reach the cloud VMs that eval runs execute on, and how <code>scp</code> and <code>rsync</code> move results back. Two audit points: a private key or agent socket left inside a task image is a credential the model can use, and the first-connection host-key question is an interactive prompt that stalls automation. The course's VM lab uses SSH; see <a href='pages/01-lab-setup.html'>page 1</a>.",
    "also": "Secure Shell, OpenSSH",
    "see": [
      "shell",
      "port",
      "secret",
      "interactive-prompt",
      "tmux"
    ]
  },
  "gnu-coreutils": {
    "name": "GNU coreutils",
    "short": "The GNU project's implementations of the basic Unix commands, such as ls, cp, cat, and sort, that ship with Ubuntu, Debian, and most mainstream Linux distributions.",
    "def": "The everyday commands are not part of the Linux kernel; they are separate programs, and on Ubuntu and Debian most of them come from one package, GNU coreutils. Related GNU packages supply <code>grep</code>, <code>sed</code>, <code>find</code>, and <code>tar</code>. GNU versions are feature-rich: long <code>--options</code>, extras such as <code>sort -h</code> or <code>date -d</code>. The reason to know the name is that it is one of three families. macOS ships BSD versions with different options; Alpine ships BusyBox versions with fewer. A command line is only portable across all three if it sticks to what POSIX specifies. So when the same command works in one task image and fails in another, <code>ls --version</code> (GNU answers, the others usually complain) is a quick way to learn which family you are talking to. See <a href='appendices/e-macos-vs-linux.html'>Appendix E</a>.",
    "also": "coreutils, GNU userland",
    "see": [
      "busybox",
      "posix",
      "option-flag",
      "distribution",
      "man-page"
    ]
  },
  "busybox": {
    "name": "BusyBox",
    "short": "A single small program that provides cut-down versions of hundreds of standard Unix commands; it is the userland of Alpine Linux and many minimal containers.",
    "def": "BusyBox packs simplified versions of <code>sh</code>, <code>ls</code>, <code>grep</code>, <code>sed</code>, <code>tar</code>, and many more into one executable; each command name is a symlink to it (in <code>alpine:3.20</code>, <code>/bin/ls</code> and <code>/bin/sh</code> both point to <code>/bin/busybox</code>), and it behaves according to the name it was called by. It exists to make very small systems, which is why Alpine-based images are a few megabytes. The trade-off is compatibility: the shell is <code>ash</code>, not bash, and the tools lack many GNU options. Agents trained mostly on Ubuntu-style transcripts issue bash-specific syntax or GNU-only flags and get <code>unrecognized option</code> or <code>not found</code>. When you see those in a trajectory, check the base image before blaming the model. See <a href='pages/15-packages-reproducibility.html'>page 15</a> and <a href='pages/27-reading-terminal-transcripts.html'>page 27</a>.",
    "also": "ash",
    "see": [
      "alpine",
      "gnu-coreutils",
      "bash",
      "posix",
      "base-image"
    ]
  },
  "posix": {
    "name": "POSIX",
    "short": "The formal standard that defines the common behaviour of Unix-like systems, including the sh language and the core commands, so that scripts and programs are portable.",
    "def": "POSIX is an IEEE/Open Group standard describing what a Unix-like system must provide: the system-call interface, the <code>sh</code> command language, and the behaviour and options of utilities such as <code>grep</code>, <code>sed</code>, and <code>find</code>. It exists because Unix fragmented into many vendors' variants and software needed a common floor. Linux with GNU tools, macOS, and BusyBox all aim at that floor and then add their own extensions. &ldquo;POSIX sh&rdquo; therefore means the portable subset: no arrays, no <code>[[ ]]</code>, no <code>pipefail</code> guarantee. On Ubuntu <code>/bin/sh</code> is <code>dash</code>, which is close to that subset, so a script with <code>#!/bin/sh</code> that uses bash features fails there even though bash is installed. If a task's scripts must run across varied images, write to POSIX or pin the interpreter explicitly. See <a href='pages/06-shell-scripting.html'>page 6</a> and <a href='appendices/e-macos-vs-linux.html'>Appendix E</a>.",
    "also": "Portable Operating System Interface, SUS",
    "see": [
      "bash",
      "shell",
      "gnu-coreutils",
      "busybox",
      "shebang"
    ]
  },
  "filesystem": {
    "name": "Filesystem",
    "short": "Either the single directory tree starting at / that holds every file on a Linux system, or a particular on-disk format (such as ext4) that stores files.",
    "def": "The word has two meanings and the course uses both. First, <em>the</em> filesystem: the one tree of directories rooted at <code>/</code> that every path is resolved in; Linux has no drive letters. Second, <em>a</em> filesystem: one organised store of files &mdash; an ext4 partition, a RAM-backed tmpfs, the virtual <code>/proc</code> &mdash; that gets attached to the tree at a directory by <a href='pages/14-mounts-and-filesystems.html'>mounting</a>. The tree you see is therefore a patchwork of several filesystems with different properties: some persistent, some wiped on restart, some read-only, some shared with the host. For an eval, those properties decide what the agent can change and what survives between episodes, which is why <code>findmnt</code> is one of the first commands in an audit. The tree itself is introduced on <a href='pages/03-files-and-the-tree.html'>page 3</a>.",
    "also": "file system, fs",
    "see": [
      "mount",
      "fhs",
      "root-directory",
      "inode",
      "overlayfs"
    ]
  },
  "fhs": {
    "name": "Filesystem Hierarchy Standard (FHS)",
    "short": "The convention that says what belongs in each top-level Linux directory, such as configuration in /etc, logs in /var/log, and programs in /usr/bin.",
    "def": "The FHS is a published convention for the layout of the directory tree, followed closely by Debian and Ubuntu. The parts worth knowing: <code>/etc</code> holds system configuration, <code>/var</code> holds data that changes (logs in <code>/var/log</code>, package state in <code>/var/lib</code>), <code>/usr</code> holds installed software, <code>/home</code> holds users' files, <code>/tmp</code> is scratch space, and <code>/proc</code>, <code>/sys</code>, and <code>/dev</code> are windows onto the kernel rather than stored files. On current Ubuntu, <code>/bin</code> is a symlink to <code>usr/bin</code>. The standard exists so that people and software can find things on a machine they have never seen &mdash; which is precisely the ten-minute-audit situation. It also gives you a baseline: a task's answer key sitting in <code>/opt/solution</code> or tests under <code>/root</code> are things an agent that knows the layout will look for. See <a href='pages/03-files-and-the-tree.html'>page 3</a>.",
    "also": "Filesystem Hierarchy Standard, directory layout",
    "see": [
      "root-directory",
      "filesystem",
      "tmp-directory",
      "proc-filesystem",
      "home-directory"
    ]
  },
  "root-directory": {
    "name": "Root Directory",
    "short": "The top of the Linux directory tree, written as a single slash (/); every absolute path starts from it. Not the same as the root user or /root.",
    "def": "<code>/</code> is the directory that contains everything else; every absolute path begins there. Three different things are called &ldquo;root&rdquo; and mixing them up causes real confusion: the root directory <code>/</code>; the root <em>user</em> (UID 0); and <code>/root</code>, which is merely the root user's home directory. What a process sees as <code>/</code> is not fixed. A container's root directory is a directory tree assembled from image layers, switched in with a mechanism descended from <code>chroot</code>, so <code>/etc/passwd</code> inside the container and on the host are unrelated files. When reading a harness's configuration, always ask &ldquo;whose <code>/</code>?&rdquo; about each path. Introduced on <a href='pages/03-files-and-the-tree.html'>page 3</a>; how a container gets its own on <a href='pages/20-namespaces.html'>page 20</a>.",
    "also": "/, slash, rootfs",
    "see": [
      "absolute-path",
      "fhs",
      "root-user",
      "chroot",
      "mount-namespace"
    ]
  },
  "inode": {
    "name": "Inode",
    "short": "The on-disk record that actually is a file: its type, owner, permissions, size, timestamps, and data location. Filenames are just directory entries pointing to inodes.",
    "def": "A file's identity is its inode, a numbered record holding everything about the file except its name: type, owner, group, permission bits, size, timestamps, link count, and where the data blocks are. A directory is a table mapping names to inode numbers. Separating name from file explains a lot: renaming within a filesystem is instant because only a directory entry changes; one file can have several names (hard links); and deleting a name only frees the data when the link count reaches zero <em>and</em> no process still has it open. <code>ls -i</code> and <code>stat</code> show inode details. A filesystem has a fixed supply, so a job that creates millions of tiny files can fail with <code>No space left on device</code> while <code>df -h</code> shows free space; <code>df -i</code> reveals it. See <a href='pages/03-files-and-the-tree.html'>page 3</a>.",
    "also": "index node",
    "see": [
      "hard-link",
      "symlink",
      "filesystem",
      "disk-usage",
      "permission-bits"
    ]
  },
  "hard-link": {
    "name": "Hard Link",
    "short": "An additional directory entry pointing at the same inode as an existing file, so one file has two equally real names and lives until the last is removed.",
    "def": "<code>ln target newname</code> creates a second name for the same inode. Neither name is &ldquo;the original&rdquo;: both show the same inode number in <code>ls -li</code>, the link count goes to 2, edits through one are visible through the other, and the data remains until every name is removed. Because a hard link refers to an inode number, it cannot cross from one filesystem to another, and you cannot hard-link directories. You will rarely create them, but they explain behaviour you will meet: why <code>rm</code> is really &ldquo;unlink&rdquo;, why deleting a file someone else has linked does not destroy the content, and how some backup and package tools save space. For integrity audits, note that removing the visible copy of an answer file does not remove a second link to it elsewhere on the same filesystem. See <a href='pages/03-files-and-the-tree.html'>page 3</a>.",
    "also": "link",
    "see": [
      "inode",
      "symlink",
      "filesystem",
      "solution-leakage"
    ]
  },
  "symlink": {
    "name": "Symbolic Link",
    "short": "A small special file containing a path to another file or directory; opening it transparently follows that path, and it breaks if the target goes away.",
    "def": "A symlink (<code>ln -s target name</code>) stores a path as text. When a program opens it, the kernel follows the stored path instead. Unlike a hard link, it can point at directories, across filesystems, or at something that does not exist &mdash; a dangling link, which produces a puzzling <code>No such file or directory</code> for a name that <code>ls</code> clearly shows. <code>ls -l</code> displays links as <code>name -&gt; target</code>, and <code>readlink -f</code> resolves the whole chain. Symlinks cross boundaries that are easy to forget: a link inside a bind-mounted workspace is resolved in whichever filesystem view the reader has, so a scorer on the host that follows an agent-created link may read a file the agent chose. Treat links in agent-writable directories as untrusted input. See <a href='pages/03-files-and-the-tree.html'>page 3</a> and <a href='pages/26-environment-integrity.html'>page 26</a>.",
    "also": "symbolic link, soft link",
    "see": [
      "hard-link",
      "inode",
      "bind-mount",
      "relative-path",
      "environment-integrity"
    ]
  },
  "dotfile": {
    "name": "Dotfile",
    "short": "A file or directory whose name begins with a dot, such as .bashrc or .git; ls and the * wildcard skip it by default, so it is 'hidden' by convention.",
    "def": "Names that begin with <code>.</code> are left out by plain <code>ls</code> and are not matched by the <code>*</code> glob; <code>ls -a</code> shows them. There is no hidden attribute and no protection &mdash; it is purely a display convention, used mainly for per-user configuration (<code>~/.bashrc</code>, <code>~/.ssh</code>) and tool metadata (<code>.git</code>, <code>.env</code>, <code>.venv</code>). The convention hides things from <em>you</em> more effectively than from an agent. A reviewer who inspects a task directory with <code>ls</code> and sees only source and tests may miss a <code>.git</code> directory whose history contains the fix, or a <code>.env</code> with an API key, both of which an agent running <code>ls -la</code> finds in one step. Always audit with <code>-a</code>. See <a href='pages/03-files-and-the-tree.html'>page 3</a> and <a href='pages/26-environment-integrity.html'>page 26</a>.",
    "also": "hidden file",
    "see": [
      "glob",
      "home-directory",
      "git-history-leak",
      "secret",
      "alias"
    ]
  },
  "everything-is-a-file": {
    "name": "Everything Is a File",
    "short": "The Unix design idea that devices, pipes, sockets, and kernel information are all accessed through the same open, read, write, and close operations used for ordinary files.",
    "def": "On Linux, a disk, a terminal, a pipe, a network connection, and a table of kernel statistics can all be opened and read like a file, and many of them appear as paths: <code>/dev/sda</code>, <code>/dev/null</code>, <code>/proc/meminfo</code>. The payoff is that one small set of tools works on everything &mdash; you can <code>cat</code> a process's environment, <code>echo</code> a value into a kernel setting, or redirect output to a device &mdash; and that one permission model guards it all. It is an approximation (network interfaces have no file, for instance), but it is the right starting assumption. It is also why file permissions and mounts are security controls in a sandbox: access to a &ldquo;file&rdquo; such as <code>/var/run/docker.sock</code> is access to the service behind it. See <a href='pages/04-streams-pipes-redirection.html'>page 4</a> and <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "see": [
      "file-descriptor",
      "device-file",
      "proc-filesystem",
      "sysfs",
      "docker-socket"
    ]
  },
  "device-file": {
    "name": "Device File",
    "short": "A special file under /dev that stands for a piece of hardware or a kernel facility; reading or writing it talks to a driver rather than to stored data.",
    "def": "Entries in <code>/dev</code> are not stored data; each is a handle to a kernel driver, identified by a major and minor number. <code>ls -l</code> marks them with <code>c</code> (character devices, read as a byte stream: terminals, <code>/dev/null</code>, <code>/dev/urandom</code>) or <code>b</code> (block devices: disks). <code>/dev/null</code>, for example, shows as <code>crw-rw-rw- &hellip; 1, 3</code>. Because a device file is the doorway to hardware, which ones exist in a sandbox is part of its security posture. A default Docker container gets a small, safe <code>/dev</code>. A container started with <code>--privileged</code> or <code>--device</code> can see host devices, including the disks that hold the host's filesystem, and that is one reason privileged containers are not an isolation boundary. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a> and <a href='pages/23-hardening-containers.html'>page 23</a>.",
    "also": "device node, special file, /dev",
    "see": [
      "dev-null",
      "block-device",
      "everything-is-a-file",
      "privileged-container",
      "tty"
    ]
  },
  "dev-null": {
    "name": "/dev/null",
    "short": "A special file that throws away anything written to it and returns end-of-file when read; used to silence output or supply empty input.",
    "def": "<code>/dev/null</code> is a device whose driver discards every write and answers every read with &ldquo;no more data&rdquo;. It exists so that &ldquo;nowhere&rdquo; can be named wherever a file is expected: <code>cmd &gt; /dev/null</code> drops stdout, <code>2&gt; /dev/null</code> drops errors, <code>&gt; /dev/null 2&gt;&amp;1</code> drops both, and <code>cmd &lt; /dev/null</code> gives a program empty input so it cannot wait on a keyboard. Convenient, and a common way to destroy evidence. A setup script that sends stderr to <code>/dev/null</code> hides the one line that would have explained why the environment is broken, and an agent that appends <code>2&gt;/dev/null</code> out of habit blinds itself to its own errors. When a transcript shows a failing command with no message, look for it. Taught on <a href='pages/04-streams-pipes-redirection.html'>page 4</a>.",
    "also": "the bit bucket, null device",
    "see": [
      "redirection",
      "stderr",
      "stdin",
      "device-file"
    ]
  },
  "proc-filesystem": {
    "name": "/proc",
    "short": "A virtual filesystem, generated on the fly by the kernel, that exposes information about every running process and about the system as readable files.",
    "def": "Nothing in <code>/proc</code> is on disk; the kernel produces the contents at the moment you read. Each process has a directory <code>/proc/PID</code> containing its command line (<code>cmdline</code>), environment (<code>environ</code>), working directory (<code>cwd</code>), open descriptors (<code>fd/</code>), and status, and <code>/proc/self</code> always refers to the reader. System-wide files such as <code>/proc/meminfo</code> and <code>/proc/mounts</code> sit alongside. Tools like <code>ps</code> and <code>top</code> are just readers of <code>/proc</code>. Two eval-relevant facts: <code>environ</code> is how secrets passed as environment variables leak to anything running as the same user, and <code>/proc/meminfo</code> inside a container reports the <em>host's</em> memory, not the cgroup limit, so a program that sizes itself from it can be OOM-killed. See <a href='pages/09-processes.html'>page 9</a>, <a href='pages/11-environment-and-secrets.html'>page 11</a>, and <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "procfs, /proc",
    "see": [
      "process",
      "pid",
      "environment-variable",
      "sysfs",
      "oom-killer"
    ]
  },
  "sysfs": {
    "name": "sysfs (/sys)",
    "short": "A virtual filesystem mounted at /sys through which the kernel exposes devices, drivers, and tunable settings as a tree of small files.",
    "def": "<code>/sys</code> is a sibling of <code>/proc</code>: also generated by the kernel, but organised around devices and kernel subsystems rather than processes. Each file typically holds a single value, and some are writable, so configuration is done with <code>cat</code> and <code>echo</code>. For this course its most important resident is the cgroup filesystem at <code>/sys/fs/cgroup</code>, where a container's real resource limits live: <code>memory.max</code>, <code>cpu.max</code>, <code>pids.max</code>. When <code>/proc/meminfo</code> shows the host's memory, <code>/sys/fs/cgroup/memory.max</code> shows what the sandbox is actually allowed. In an unprivileged Docker container <code>/sys</code> is mounted read-only, so processes inside can read their limits but not raise them; a writable <code>/sys</code> is a sign of a privileged container. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a> and <a href='pages/21-cgroups-capabilities-seccomp.html'>page 21</a>.",
    "also": "/sys",
    "see": [
      "proc-filesystem",
      "cgroup",
      "read-only-mount",
      "everything-is-a-file",
      "privileged-container"
    ]
  },
  "tmp-directory": {
    "name": "/tmp",
    "short": "The system-wide scratch directory that any user may write to; its contents are temporary and should not be expected to survive a reboot.",
    "def": "<code>/tmp</code> is where programs put short-lived files. Its mode is <code>drwxrwxrwt</code> (octal 1777): world-writable so every user can create files there, with the <a href='pages/08-permissions.html'>sticky bit</a> so that users cannot delete one another's. Because it is always present and always writable, it is where things end up when nowhere else works &mdash; including in a container whose root filesystem is read-only, where <code>/tmp</code> is usually given its own tmpfs mount so software can still function. That same openness makes it shared ground. If the agent and the verifier run in the same container, anything the verifier stages in <code>/tmp</code> is readable, and often replaceable, by the agent; and if a sandbox is reused without a proper reset, files left in <code>/tmp</code> carry one episode's work into the next. See <a href='pages/03-files-and-the-tree.html'>page 3</a> and <a href='pages/26-environment-integrity.html'>page 26</a>.",
    "also": "temporary directory, TMPDIR",
    "see": [
      "sticky-bit",
      "tmpfs",
      "fhs",
      "reset",
      "read-only-mount"
    ]
  },
  "mount": {
    "name": "Mount",
    "short": "To attach a filesystem, such as a disk partition, a RAM disk, or a host directory, to a directory in the tree so its contents appear there.",
    "def": "Linux has one directory tree, so storage joins it by being mounted: <code>mount /dev/sdb1 /data</code> makes the filesystem on that partition appear under <code>/data</code>. The kernel keeps a mount table recording, for each mount, its source, target directory, filesystem type, and options such as <code>ro</code>, <code>nosuid</code>, and <code>noexec</code>. <code>findmnt</code> prints it as a tree; <code>/proc/mounts</code> is the raw form. That table is the ground truth about a sandbox's storage, and reading it answers the audit questions directly: which directories come from the host, which are read-only, which are RAM-backed and vanish, which persist. Containers each get their own mount table through a mount namespace, which is how their <code>/</code> differs from the host's. Taught on <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "mounting, mount table",
    "see": [
      "mount-point",
      "bind-mount",
      "read-only-mount",
      "mount-namespace",
      "filesystem"
    ]
  },
  "mount-point": {
    "name": "Mount Point",
    "short": "The directory at which a filesystem is attached to the tree; while the mount is in place, whatever the directory held before is hidden beneath it.",
    "def": "A mount point is an ordinary directory chosen as the place where a mounted filesystem appears. From then on, paths passing through it cross into the mounted filesystem. Anything that was in the directory beforehand is not deleted, only hidden until the unmount. That shadowing effect explains a recurring container surprise: an image ships files in <code>/app</code>, someone runs it with a bind mount or empty volume over <code>/app</code>, and the image's files seem to have vanished. It also sets boundaries that tools respect &mdash; <code>df</code> reports space per mounted filesystem, hard links cannot cross a mount point, and <code>find -xdev</code> stops at them. In an audit, <code>findmnt --target /some/path</code> tells you which mount a given path really lives on. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "mountpoint",
    "see": [
      "mount",
      "bind-mount",
      "volume",
      "hard-link",
      "disk-usage"
    ]
  },
  "bind-mount": {
    "name": "Bind Mount",
    "short": "A mount that makes an existing directory or file appear at a second location; Docker uses it to share a host directory with a container.",
    "def": "An ordinary mount attaches a device; a bind mount attaches a directory that is already in the tree to another place, so the same files are reachable by two paths, with no copy: a write through either path is immediately visible through the other. <code>docker run -v /host/dir:/container/dir</code> is a bind mount across the container boundary, and it is the usual way a harness hands a repository to the agent and gets results back. It is also a deliberate hole in the sandbox wall. Writes land on the host with the container process's numeric UID (often root's); anything in the host directory is exposed, including tests or solutions stored beside the task; and mounting <code>/var/run/docker.sock</code> this way hands the container control of the host's Docker. Mount only what is needed, read-only where possible. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a> and <a href='pages/22-docker-for-evals.html'>page 22</a>.",
    "also": "-v host:container, --mount type=bind",
    "see": [
      "mount",
      "volume",
      "read-only-mount",
      "docker-socket",
      "uid"
    ]
  },
  "read-only-mount": {
    "name": "Read-Only Mount",
    "short": "A filesystem mounted with the ro option, so the kernel refuses every attempt to create, change, or delete files on it, even by root.",
    "def": "The <code>ro</code> mount option makes the kernel reject all writes to that filesystem with the error <code>Read-only file system</code>. Unlike permission bits, which root bypasses, this applies to every user, which is what makes it useful in a sandbox where the agent often is root. Docker exposes it in two ways: <code>:ro</code> on an individual bind mount or volume, and <code>--read-only</code> for the container's whole root filesystem, normally paired with a tmpfs at <code>/tmp</code> so programs still have scratch space. For eval integrity this is the simplest strong control there is: tests, fixtures, and scoring scripts mounted read-only cannot be edited by the agent. Verify rather than assume &mdash; the <code>OPTIONS</code> column of <code>findmnt</code> shows <code>ro</code> or <code>rw</code> for each mount. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a> and <a href='pages/23-hardening-containers.html'>page 23</a>.",
    "also": "ro, read-only filesystem, EROFS",
    "see": [
      "mount",
      "bind-mount",
      "tmpfs",
      "test-tampering",
      "root-user"
    ]
  },
  "tmpfs": {
    "name": "tmpfs",
    "short": "A filesystem that lives in memory rather than on disk: fast, size-limited, and completely erased when it is unmounted or the machine or container stops.",
    "def": "tmpfs stores files in RAM (spilling to swap if there is any). It is used where data should be fast and should not persist: <code>/run</code>, <code>/dev/shm</code>, and often <code>/tmp</code>. In Docker, <code>--tmpfs /tmp</code> adds one, and every container gets a small <code>/dev/shm</code>, 64 MB by default. Two properties matter for evals. It gives a guaranteed-clean scratch area: nothing written there can leak into the next episode once the container is gone. And its contents use memory, not disk, so a job that writes large files to a tmpfs is spending the sandbox's memory allowance and can end up killed for it rather than getting a tidy &ldquo;disk full&rdquo; error. The too-small <code>/dev/shm</code> is also a classic cause of browsers and multiprocess Python crashing in containers. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "RAM disk, /dev/shm",
    "see": [
      "mount",
      "tmp-directory",
      "read-only-mount",
      "oom-killer",
      "memory-rss"
    ]
  },
  "overlayfs": {
    "name": "OverlayFS",
    "short": "A filesystem that stacks a writable layer on top of read-only layers and presents the merged result; it is how Docker builds a container's root filesystem.",
    "def": "OverlayFS merges directories: one or more read-only <em>lower</em> layers and one writable <em>upper</em> layer, shown as a single tree. Reads fall through to whichever layer has the file. The first write to a lower-layer file copies it up into the upper layer and changes the copy; a deletion is recorded as a marker in the upper layer. Many containers can therefore share one set of image layers, each adding only a thin upper layer, visible as <code>overlay on /</code> in <code>mount</code> output. For evals it is the reset mechanism &mdash; remove the container and the upper layer goes with it, restoring the image state. The flip side: files &ldquo;deleted&rdquo; in a later image layer still exist in an earlier one, so secrets and solutions removed that way remain recoverable from the image. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a> and <a href='pages/22-docker-for-evals.html'>page 22</a>.",
    "also": "overlay, overlay2, union filesystem",
    "see": [
      "layer",
      "image",
      "container",
      "reset",
      "solution-leakage"
    ]
  },
  "volume": {
    "name": "Volume",
    "short": "Storage that Docker creates and manages outside any single container's writable layer, so the data persists when the container is removed and can be shared.",
    "def": "A container's own filesystem disappears when the container is removed. A volume is Docker's answer for data that should outlive it: a directory Docker manages on the host, attached at a path in the container with <code>-v name:/path</code>, and listed with <code>docker volume ls</code>. It differs from a bind mount in that you name the volume, not a host path, so it does not depend on the host's directory layout. Persistence is the feature and, for evals, the hazard. A named volume reused across runs carries state from one episode into the next &mdash; caches, databases, half-finished work &mdash; and quietly breaks the assumption that every rollout starts from the same place. <code>docker compose down</code> leaves volumes in place unless you add <code>-v</code>. For eval tasks, prefer fresh volumes per run. See <a href='pages/22-docker-for-evals.html'>page 22</a>.",
    "also": "Docker volume, named volume",
    "see": [
      "bind-mount",
      "mount",
      "reset",
      "docker-compose",
      "nondeterminism"
    ]
  },
  "block-device": {
    "name": "Block Device",
    "short": "A storage device, such as a disk, SSD, or partition, that the kernel reads and writes in fixed-size blocks; filesystems are created on top of block devices.",
    "def": "A block device is raw storage addressed by block number: a physical or virtual disk (<code>/dev/sda</code>, <code>/dev/nvme0n1</code>, <code>/dev/vda</code> in a VM) or a partition of one (<code>/dev/sda1</code>). On its own it has no files; you create a filesystem on it and then mount that. <code>lsblk</code> draws the picture: each device, its size, its partitions, and where each is mounted. The layering is worth holding in your head &mdash; hardware, block device, filesystem, mount point, path &mdash; because &ldquo;the disk is full&rdquo; or &ldquo;the file is missing&rdquo; can be a problem at any of those levels. On a VM you will see real block devices. Inside an ordinary container you mostly will not, because the container is given directories, not disks; seeing the host's disks under <code>/dev</code> indicates a privileged container. See <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "disk, partition, lsblk",
    "see": [
      "device-file",
      "filesystem",
      "mount",
      "disk-usage",
      "privileged-container"
    ]
  },
  "disk-usage": {
    "name": "Disk Usage",
    "short": "How much storage is used and free, measured per filesystem with df and per directory with du; the two can legitimately disagree.",
    "def": "Two commands answer two different questions. <code>df -h</code> asks each mounted filesystem how full it is. <code>du -sh dir</code> walks a directory and adds up the files it finds. They diverge when space is held by something <code>du</code> cannot see, most often a large file that was deleted while a process still has it open; the space is released only when that process closes it or exits. A full filesystem produces <code>No space left on device</code>, and the same message appears when a filesystem runs out of inodes (<code>df -i</code>). Disk exhaustion is a classic infrastructure failure in eval runs: image layers, logs, and leftover containers fill the host, after which every task fails at <code>pip install</code> or on its first write, and the results look like a sudden capability collapse. See <a href='pages/12-resources-and-limits.html'>page 12</a> and <a href='pages/14-mounts-and-filesystems.html'>page 14</a>.",
    "also": "df, du, ENOSPC",
    "see": [
      "inode",
      "mount-point",
      "filesystem",
      "infrastructure-failure",
      "file-descriptor"
    ]
  },
  "user": {
    "name": "User",
    "short": "An account identity that processes run as and files are owned by; to the kernel a user is just a number (the UID), and the name is a label looked up in /etc/passwd.",
    "def": "A Linux user is not necessarily a person. It is an identity attached to every process and every file, and the kernel compares the two to decide what a process may do. Some users are people with a password and a home directory; many are accounts that exist only so that a service runs with its own limited identity. The kernel deals only in numeric IDs; names such as <code>alice</code> or <code>www-data</code> come from <code>/etc/passwd</code> and exist for humans. <code>whoami</code> and <code>id</code> show who you are. In eval work the question &ldquo;which user does the agent run as?&rdquo; is a design decision with consequences: as root, the agent can edit tests, read anything in the container, and install anything; as an unprivileged user, some legitimate tasks (such as <code>apt-get install</code>) become impossible. Taught on <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "account, user account",
    "see": [
      "uid",
      "group",
      "root-user",
      "passwd-file",
      "service-account"
    ]
  },
  "uid": {
    "name": "UID",
    "short": "User ID: the number the kernel actually uses to identify a user. UID 0 is root; ordinary accounts on Ubuntu start at 1000.",
    "def": "Every process carries a UID and every file records its owner's UID; permission checks compare the numbers. The mapping from number to name lives in <code>/etc/passwd</code> and is local to each system &mdash; or each container image. UID 0 is root. On Ubuntu, system accounts take low numbers and the first ordinary user gets 1000; the <code>ubuntu:24.04</code> image ships a user <code>ubuntu</code> with UID 1000. Because only the number is real, identity does not translate across a bind mount: a file created by UID 1000 in a container belongs on the host to whoever is UID 1000 there, and files written by a container's root are owned by root on the host. That is the source of most &ldquo;permission denied on the results directory&rdquo; harness bugs. <code>ls -ln</code> shows numeric owners. See <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "user ID",
    "see": [
      "user",
      "gid",
      "root-user",
      "passwd-file",
      "user-namespace"
    ]
  },
  "gid": {
    "name": "GID",
    "short": "Group ID: the number the kernel uses to identify a group. Each process has a primary GID plus a list of supplementary ones, and each file records one owning GID.",
    "def": "A GID is to a group what a UID is to a user: the number that is actually stored and compared, with names supplied by <code>/etc/group</code>. A process has one primary GID, which new files it creates are stamped with, and a list of supplementary GIDs for the other groups its user belongs to; <code>id</code> prints all of them. A file has exactly one owning GID, and the middle three permission bits apply to processes holding it. Like UIDs, GIDs are only numbers and do not carry meaning across the container boundary: GID 999 might be <code>docker</code> on the host and something unrelated, or nothing, inside the image. When <code>ls -l</code> shows a bare number where a group name should be, the file's GID simply has no entry in this system's <code>/etc/group</code>. See <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "group ID",
    "see": [
      "group",
      "uid",
      "permission-bits",
      "chown"
    ]
  },
  "group": {
    "name": "Group",
    "short": "A named set of users, used to give several accounts the same access to files or devices without making those files open to everyone.",
    "def": "Permission bits offer three audiences: the owner, one group, and everyone else. Groups are how you say &ldquo;these particular accounts, but not the world&rdquo;. Membership is listed in <code>/etc/group</code>; each user has a primary group (on Ubuntu, a private group with the same name as the user) and any number of supplementary ones, all shown by <code>id</code>. Membership is read at login, so a newly added group takes effect only in a new session. Some groups carry real power: members of <code>sudo</code> may run commands as root, <code>shadow</code> may read password hashes, and <code>docker</code> may talk to the Docker daemon, which Docker's own documentation describes as root-equivalent access to the host. When auditing an account, read its group list as carefully as its UID. Taught on <a href='pages/07-users-groups-root.html'>page 7</a> and applied on <a href='pages/08-permissions.html'>page 8</a>.",
    "see": [
      "gid",
      "user",
      "permission-bits",
      "sudo",
      "docker-socket"
    ]
  },
  "root-user": {
    "name": "Root (Superuser)",
    "short": "The administrative account with UID 0, for which the kernel skips ordinary file permission checks; the default user inside most Docker containers.",
    "def": "Root is whichever account has UID 0. The kernel exempts it from file permission checks and lets it perform privileged operations: binding low ports, mounting filesystems, changing file ownership, signalling any process. A file with mode <code>444</code> is still writable by root. It exists because something has to administer the machine; the convention is to use it as little as possible. Containers invert that: unless the image sets <code>USER</code>, a Docker container's processes run as root. That root is reduced &mdash; Docker removes many capabilities and confines it with namespaces &mdash; but within the container it still overrides every permission bit. So an agent running as root cannot be stopped from editing tests by <code>chmod</code>; you need a non-root user, a read-only mount, or tests held outside the sandbox. See <a href='pages/07-users-groups-root.html'>page 7</a> and <a href='pages/23-hardening-containers.html'>page 23</a>.",
    "also": "superuser, UID 0, root",
    "see": [
      "uid",
      "sudo",
      "capability",
      "least-privilege",
      "read-only-mount"
    ]
  },
  "sudo": {
    "name": "sudo",
    "short": "A command that runs another command as root (or another user) if the rules in /etc/sudoers allow the caller to do so, usually after asking for a password.",
    "def": "<code>sudo cmd</code> lets a permitted user run one command with root's identity instead of logging in as root. The rules live in <code>/etc/sudoers</code> and <code>/etc/sudoers.d/</code>; on Ubuntu, members of the <code>sudo</code> group may run anything. It works because the <code>sudo</code> binary is setuid root: it starts with root's privileges and then decides whether to honour the request. It gives a machine with several administrators accountability and a habit of least privilege. In containers, expect it to be missing &mdash; the <code>ubuntu:24.04</code> image does not include it, and as root you do not need it &mdash; so an agent that prefixes every command with <code>sudo</code> collects <code>command not found</code> errors. The opposite problem is worse: a task image that grants its &ldquo;unprivileged&rdquo; agent user passwordless sudo (<code>NOPASSWD: ALL</code>) has no privilege separation at all. See <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "su, sudoers",
    "see": [
      "root-user",
      "setuid",
      "privilege-escalation",
      "least-privilege",
      "group"
    ]
  },
  "passwd-file": {
    "name": "/etc/passwd",
    "short": "The world-readable text file listing every user account: name, UID, primary GID, home directory, and login shell. Despite the name it holds no passwords.",
    "def": "Each line of <code>/etc/passwd</code> describes one account in seven colon-separated fields: name, password placeholder, UID, GID, comment, home directory, and login shell &mdash; for example <code>root:x:0:0:root:/root:/bin/bash</code>. The <code>x</code> means the password hash is kept elsewhere, in <code>/etc/shadow</code>. The file must be readable by everyone, because any program that prints a username (such as <code>ls -l</code>) has to look the number up here; that requirement is the reason hashes were moved out. Reading it is a fast audit step: it tells you which accounts exist, which have a real shell rather than <code>/usr/sbin/nologin</code>, and whether anything besides root has UID 0. It belongs to the image, so a container started with <code>--user 1234</code> can run as a UID with no line here; tools then report <code>I have no name!</code>. Taught on <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "passwd, user database",
    "see": [
      "shadow-file",
      "uid",
      "user",
      "home-directory",
      "service-account"
    ]
  },
  "shadow-file": {
    "name": "/etc/shadow",
    "short": "The root-protected file that stores each account's hashed password and password-ageing settings, kept separate from the world-readable /etc/passwd.",
    "def": "<code>/etc/passwd</code> has to be readable by all, so password hashes were moved to <code>/etc/shadow</code>, which on Ubuntu is mode <code>640</code>, owner <code>root</code>, group <code>shadow</code>. Each line holds a username, the salted hash of the password (its prefix identifies the algorithm), and ageing fields. A <code>!</code> or <code>*</code> in the hash field means no password can match, so the account cannot log in with one; most accounts in a container image look like this. The point of hiding hashes is that anyone who can read them can try to guess passwords offline at their leisure. For sandbox audits the file is a useful indicator: if the agent's user can read <code>/etc/shadow</code>, it is either root or has more privilege than was intended. See <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "shadow passwords",
    "see": [
      "passwd-file",
      "root-user",
      "permission-bits",
      "secret"
    ]
  },
  "permission-bits": {
    "name": "Permission Bits",
    "short": "The nine flags on every file, read, write, and execute for each of owner, group, and others, that decide what a non-root process may do with it.",
    "def": "<code>ls -l</code> shows them as a string such as <code>-rwxr-x---</code>: after the type character come three triplets, for the owning user, the owning group, and everyone else. The kernel uses exactly one triplet &mdash; the first that applies to the process &mdash; and checks the bit for the requested operation. On a file, <code>r</code> is read, <code>w</code> modify, <code>x</code> execute. On a directory the meanings shift: <code>r</code> lists names, <code>x</code> allows passing through to what is inside, and <code>w</code> allows creating, renaming, and <em>deleting</em> entries. It follows that whether you can delete a file depends on the directory's permissions, not the file's &mdash; so a read-only test file in an agent-writable directory can be removed and replaced. Root bypasses all of these checks. Taught on <a href='pages/08-permissions.html'>page 8</a>.",
    "also": "file mode, rwx, mode bits",
    "see": [
      "octal-mode",
      "chmod",
      "chown",
      "umask",
      "test-tampering"
    ]
  },
  "octal-mode": {
    "name": "Octal Mode",
    "short": "Permission bits written as a three- or four-digit number such as 755 or 644, where each digit is the sum of read=4, write=2, execute=1.",
    "def": "Each permission triplet is three bits, and three bits make exactly one octal digit: <code>r</code>=4, <code>w</code>=2, <code>x</code>=1, added together. So <code>rwx</code> is 7, <code>r-x</code> is 5, <code>r--</code> is 4, and the mode <code>rwxr-xr-x</code> is <code>755</code>. The values you will see daily: <code>644</code> (owner writes, everyone reads &mdash; normal files), <code>755</code> (the same plus execute &mdash; programs and directories), <code>600</code> and <code>700</code> (owner only &mdash; keys and private directories), and <code>777</code> (anyone can do anything, nearly always a mistake). An optional leading fourth digit holds the special bits: setuid=4, setgid=2, sticky=1, as in <code>1777</code> for <code>/tmp</code>. Deriving the digits from bits means you can read any mode, including unusual ones in a Dockerfile's <code>COPY --chmod</code>. See <a href='pages/08-permissions.html'>page 8</a> and <a href='appendices/c-binary-octal-cidr.html'>Appendix C</a>.",
    "also": "numeric mode, 755, 644",
    "see": [
      "permission-bits",
      "chmod",
      "umask",
      "setuid",
      "sticky-bit"
    ]
  },
  "chmod": {
    "name": "chmod",
    "short": "The command that changes a file's permission bits, using either an octal number (chmod 644 file) or symbolic changes (chmod u+x file).",
    "def": "<code>chmod</code> (&ldquo;change mode&rdquo;) sets permission bits. The octal form replaces all of them at once: <code>chmod 600 key.pem</code>. The symbolic form adjusts some and leaves the rest: <code>chmod u+x run.sh</code> adds execute for the owner, <code>go-w</code> removes write from group and others, <code>-R</code> recurses. Only a file's owner or root may change its mode. The everyday use is <code>chmod +x script.sh</code>, the cure for <code>Permission denied</code> (exit status 126) when running a script you just wrote. Two warnings for eval builders. <code>chmod -R 777</code> to &ldquo;fix permissions&rdquo; makes every file, tests included, writable by the agent. And <code>chmod</code> is not a lock against the file's owner or root, who can simply change the mode back; protection needs a different owner or a read-only mount. Taught on <a href='pages/08-permissions.html'>page 8</a>.",
    "also": "change mode",
    "see": [
      "permission-bits",
      "octal-mode",
      "chown",
      "umask",
      "exit-status"
    ]
  },
  "chown": {
    "name": "chown",
    "short": "The command that changes which user and group own a file, as in chown alice:devs file; in general only root may give a file to another user.",
    "def": "<code>chown user:group path</code> rewrites the owner UID and group GID stored in a file's inode; <code>-R</code> applies it to a whole tree. Ownership matters because the owner triplet of the permission bits applies to the owner, and only the owner (or root) may <code>chmod</code> the file. An ordinary user cannot give files away &mdash; the attempt fails with <code>Operation not permitted</code> &mdash; so in practice this is a root operation. You meet it constantly in Dockerfiles, because files copied into an image are owned by root unless you write <code>COPY --chown=agent:agent</code>; forget it, switch to a non-root <code>USER</code>, and the agent cannot write in its own workspace. The integrity pattern runs the other way: make tests and fixtures owned by root and not writable by others, and run the agent as someone else. See <a href='pages/08-permissions.html'>page 8</a>.",
    "also": "change owner, chgrp",
    "see": [
      "uid",
      "gid",
      "permission-bits",
      "chmod",
      "dockerfile"
    ]
  },
  "umask": {
    "name": "umask",
    "short": "A per-process setting listing the permission bits to remove from newly created files and directories; the usual default, 022, yields 644 files and 755 directories.",
    "def": "When a program creates a file it requests a mode, typically <code>666</code> for files and <code>777</code> for directories, and the kernel clears whichever bits are set in the process's umask. With the common default of <code>022</code> (remove write for group and others) the results are <code>644</code> and <code>755</code>. It is inherited from parent to child, and running <code>umask</code> with no argument prints the current value; on Ubuntu an ordinary user with a private group may see <code>002</code> in a login session. It affects only creation, never existing files. If files an agent creates arrive with unexpected permissions &mdash; say, output the scorer's user cannot read &mdash; compare the umask under the harness with the one in your interactive shell. See <a href='pages/08-permissions.html'>page 8</a> and <a href='appendices/c-binary-octal-cidr.html'>Appendix C</a>.",
    "also": "file mode creation mask",
    "see": [
      "permission-bits",
      "octal-mode",
      "chmod",
      "builtin"
    ]
  },
  "setuid": {
    "name": "Setuid Bit",
    "short": "A special permission bit on an executable that makes it run with the identity of the file's owner, usually root, rather than of the user who started it.",
    "def": "Normally a program runs as whoever launched it. If an executable has the setuid bit (shown as <code>s</code> in the owner's execute position, octal <code>4000</code>), it runs with the file owner's effective UID instead. That is how an ordinary user can change their own password: <code>/usr/bin/passwd</code> is <code>-rwsr-xr-x root</code>, so it can update <code>/etc/shadow</code> on the user's behalf. <code>sudo</code> and <code>su</code> depend on the same bit. The sibling setgid bit (<code>2000</code>) does the same for the group. Each setuid-root binary is a deliberate, narrow door to root, and a bug in one &mdash; or a careless one such as a setuid copy of <code>bash</code> &mdash; becomes privilege escalation. Audit with <code>find / -perm -4000 -type f</code>, and close the door for sandboxes with the <code>nosuid</code> mount option or Docker's <code>no-new-privileges</code>. See <a href='pages/08-permissions.html'>page 8</a> and <a href='pages/23-hardening-containers.html'>page 23</a>.",
    "also": "SUID, setgid, set-user-ID",
    "see": [
      "permission-bits",
      "sudo",
      "privilege-escalation",
      "no-new-privileges",
      "octal-mode"
    ]
  },
  "sticky-bit": {
    "name": "Sticky Bit",
    "short": "A special permission bit on a directory that lets users delete or rename only their own files in it, even though everyone can write there; /tmp uses it.",
    "def": "Write permission on a directory normally lets you delete any entry in it, whoever owns the file. For a shared directory such as <code>/tmp</code> that would let users destroy each other's work. The sticky bit (octal <code>1000</code>, shown as a <code>t</code> at the end of the mode: <code>drwxrwxrwt</code>) adds one rule: an entry may be removed or renamed only by the file's owner, the directory's owner, or root. The name is a leftover from an unrelated older meaning. It is the right setting for any directory several unprivileged identities share &mdash; for example a drop-box where an agent user and a verifier user both write. Without it, either side can remove and replace the other's files despite not being able to modify them. It does not restrain root. See <a href='pages/08-permissions.html'>page 8</a>.",
    "also": "restricted deletion flag, 1777",
    "see": [
      "tmp-directory",
      "permission-bits",
      "octal-mode",
      "setuid"
    ]
  },
  "least-privilege": {
    "name": "Principle of Least Privilege",
    "short": "The design rule that every user, process, and container should hold only the permissions it needs for its job, so mistakes and compromises do limited damage.",
    "def": "Least privilege means granting the minimum access a job requires . The argument is containment: whatever a process is <em>able</em> to do is what a bug, a compromise, or an over-eager agent will eventually do with it. On Linux the principle is applied in layers &mdash; a non-root user, tight file ownership and modes, read-only mounts, dropped capabilities, no network unless the task needs one, resource limits. For evals it serves two purposes. It protects your infrastructure from the code the model writes. And it protects the <em>measurement</em>: an agent that cannot write to the tests, read the solution, or reach the internet cannot score by those routes, so a pass means what you think it means. The cost is real (too little privilege blocks legitimate work), so record what each task needs. See <a href='pages/23-hardening-containers.html'>page 23</a> and <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "PoLP, minimal privilege",
    "see": [
      "root-user",
      "capability",
      "privilege-escalation",
      "attack-surface",
      "environment-integrity"
    ]
  },
  "privilege-escalation": {
    "name": "Privilege Escalation",
    "short": "Gaining more access than you were given, typically an ordinary user becoming root, or a process inside a container gaining control of the host.",
    "def": "Privilege escalation is any path from the access a process was granted to access it was not. On a single machine it usually means unprivileged user to root: a permissive sudo rule, a vulnerable or unnecessary setuid binary, a root-run script that an ordinary user can edit, membership of the <code>docker</code> group. In a sandbox there is a second step, from inside the container to the host, through a mounted Docker socket, a <code>--privileged</code> flag, or a kernel bug. You need the concept for defence, not attack: when designing an environment, ask what the agent's user could reach if it tried, and close those paths before the run. A capable agent that wants <code>apt-get</code> to work may well try <code>sudo</code>, look for writable root-owned scripts, or probe the socket. See <a href='pages/23-hardening-containers.html'>page 23</a> and <a href='pages/08-permissions.html'>page 8</a>.",
    "also": "privesc",
    "see": [
      "setuid",
      "sudo",
      "least-privilege",
      "container-escape",
      "docker-socket"
    ]
  },
  "service-account": {
    "name": "Service Account",
    "short": "A user account created for a program rather than a person, typically with a low UID, no password, and no login shell, so a service runs with limited rights.",
    "def": "Many lines in <code>/etc/passwd</code> are not people: <code>www-data</code> (UID 33), <code>_apt</code>, <code>nobody</code> (65534), <code>daemon</code>. Each exists so a particular piece of software can run under its own identity and own only its own files. If the web server is compromised, the attacker holds <code>www-data</code>'s limited access, not root's. Such accounts normally have a system-range UID below 1000, a locked password, and the shell <code>/usr/sbin/nologin</code>, so nobody can sign in as them. The same pattern is what you want for an agent: a Dockerfile that runs <code>useradd</code> to create a dedicated user and then sets <code>USER</code> gives the agent a service account of its own, while tests and scorer files remain owned by root. When reading <code>ps</code> output in an audit, an unexpected service running as root rather than its own account deserves a second look. See <a href='pages/07-users-groups-root.html'>page 7</a>.",
    "also": "system user, system account",
    "see": [
      "user",
      "uid",
      "passwd-file",
      "least-privilege",
      "daemon"
    ]
  },
  "process": {
    "name": "Process",
    "short": "A running instance of a program: its code in memory plus the bookkeeping the kernel keeps for it, such as an ID, an owner, open files and a working directory.",
    "def": "A program is a file on disk; a process is what you get when the kernel loads that file and runs it. Each process has its own memory, a numeric ID, an owning user, a working directory, a set of environment variables and a table of open file descriptors. Running the same program twice gives two independent processes. The kernel keeps processes apart so that one crashing or misbehaving cannot corrupt another. Everything an agent does in a sandbox is a process you can list with <code>ps</code>, which is how you answer the first audit question: what is running here? See <a href='pages/09-processes.html'>Processes: What Is Running</a>.",
    "see": [
      "pid",
      "parent-process",
      "fork-exec",
      "kernel",
      "signal"
    ]
  },
  "pid": {
    "name": "PID",
    "short": "Process ID: the number the kernel assigns to each running process, used to inspect it, signal it, or find its entry under /proc.",
    "def": "Every process gets a process ID when it is created, and the number is how every other tool refers to it: <code>kill 4312</code> signals it, <code>/proc/4312/</code> describes it, <code>ps -p 4312</code> shows it. PIDs are handed out in increasing order and eventually reused after a process is gone, so a PID identifies a process only while it is alive. Inside a container the numbering starts again from 1, because the container has its own PID namespace; the same process has a different, larger PID when seen from the host. Keep that in mind when matching harness logs against what you see inside the box. Taught in <a href='pages/09-processes.html'>Processes</a>.",
    "also": "process ID",
    "see": [
      "process",
      "pid-1",
      "pid-namespace",
      "proc-filesystem",
      "parent-process"
    ]
  },
  "parent-process": {
    "name": "Parent Process",
    "short": "The process that created another process; every process records its parent's ID (PPID), so all processes on a machine form a single tree.",
    "def": "Processes are only ever created by other processes, so each one has a parent, recorded as its PPID. Follow the parents upward and you always arrive at PID 1; the result is a tree, which <code>ps -ef --forest</code> or <code>pstree</code> will draw for you. The tree matters because a child inherits from its parent: environment variables, open file descriptors, user identity, working directory and resource limits. It is also the parent's job to collect the child's exit status. When you read a process listing in a sandbox, the tree tells you who started what — whether that stray server was launched by the harness, by the task's setup script, or by the agent. See <a href='pages/09-processes.html'>Processes</a>.",
    "also": "PPID, child process",
    "see": [
      "process",
      "pid",
      "fork-exec",
      "zombie-process",
      "orphan-process"
    ]
  },
  "fork-exec": {
    "name": "fork and exec",
    "short": "The two-step way Unix starts programs: fork copies the current process, then exec replaces the copy's program with a new one, keeping the same PID.",
    "def": "Linux has no single call meaning run this program. Instead a process calls <code>fork</code> to make a near-identical copy of itself, and the copy calls <code>exec</code> to replace its own code with a new program. The gap between the two steps is the point: the child can rearrange its file descriptors, change directory or drop privileges before the new program starts, which is exactly how a shell implements pipes and redirection. It also explains inheritance — the new program keeps the environment and open files of the process that forked it. When a transcript shows a secret or a working directory turning up in an unexpected program, inheritance across fork and exec is the mechanism. See <a href='pages/09-processes.html'>Processes</a>.",
    "also": "fork, exec, execve",
    "see": [
      "process",
      "parent-process",
      "system-call",
      "environment-variable",
      "file-descriptor"
    ]
  },
  "daemon": {
    "name": "Daemon",
    "short": "A long-running background process with no terminal attached, usually providing a service such as a web server, a database, or the Docker engine.",
    "def": "A daemon is a process meant to run indefinitely in the background rather than do a job and exit: <code>sshd</code> waiting for logins, <code>dockerd</code> managing containers, a database waiting for queries. By convention many daemon names end in d. They have no controlling terminal, so they report through log files or the journal instead of your screen, and on a full machine they are started and supervised by the init system. Containers usually have no init system, so a task that needs a database must start the daemon itself and wait until it is ready. A task that fails on every model because the service never came up is an environment bug, not a capability result. See <a href='pages/09-processes.html'>Processes</a> and <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a>.",
    "also": "service, background service",
    "see": [
      "process",
      "init",
      "systemd",
      "unit",
      "background-process"
    ]
  },
  "zombie-process": {
    "name": "Zombie Process",
    "short": "A process that has exited but whose parent has not yet collected its exit status, leaving a dead entry in the process table.",
    "def": "When a process exits, the kernel frees its memory but keeps a small record — the PID and the exit status — until the parent asks for it with <code>wait</code>. In that in-between state the process is a zombie, shown by <code>ps</code> with state <code>Z</code> or <code>&lt;defunct&gt;</code>. A zombie uses no CPU or memory and cannot be killed, because it is already dead; only the parent collecting the status, or the parent itself exiting, clears it. A handful are harmless. They pile up when the parent never waits, and each one occupies a PID slot, so a container with a process-count limit can eventually fail to start anything new. See <a href='pages/09-processes.html'>Processes</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "defunct process",
    "see": [
      "parent-process",
      "orphan-process",
      "pid-1",
      "init",
      "exit-status"
    ]
  },
  "orphan-process": {
    "name": "Orphan Process",
    "short": "A process whose parent has exited while it is still running; the kernel re-parents it, normally to PID 1.",
    "def": "If a parent exits before its child, the child carries on running and the kernel gives it a new parent — normally PID 1, whose job includes collecting the exit status of such adopted children. Orphans are not an error; deliberately orphaning yourself is how a daemon detaches from the shell that launched it. They matter in eval work because killing the process you started does not kill what it started. A harness that times out an agent's command by killing only the shell can leave the real work — a test runner, a server, a busy loop — still running, eating CPU and holding ports during the next command or the scoring step. See <a href='pages/09-processes.html'>Processes</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "see": [
      "parent-process",
      "zombie-process",
      "pid-1",
      "background-process",
      "timeout"
    ]
  },
  "pid-1": {
    "name": "PID 1",
    "short": "The first process in a machine or container; it adopts orphaned processes, gets special signal treatment from the kernel, and when it exits the container stops.",
    "def": "On a full machine PID 1 is the init system. In a container it is whatever command the image was told to run — often your application, or just <code>sleep infinity</code>. Two rules make it special. First, the kernel delivers a signal to PID 1 only if that process has installed a handler for it, so a program that never planned to be PID 1 may simply ignore SIGTERM; <code>docker stop</code> then waits out its grace period and resorts to SIGKILL. Second, orphans are re-parented to PID 1, and if it never collects them zombies accumulate. Running the container with a small init (<code>docker run --init</code>) fixes both. When PID 1 exits, the container is over. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a> and <a href='pages/20-namespaces.html'>Namespaces</a>.",
    "see": [
      "init",
      "pid-namespace",
      "zombie-process",
      "sigterm",
      "entrypoint"
    ]
  },
  "init": {
    "name": "Init",
    "short": "The first user-space process the kernel starts (PID 1), responsible for launching and supervising everything else and for cleaning up orphaned processes.",
    "def": "After the kernel finishes booting it starts exactly one program, and that program — init — starts everything else: mounting filesystems, bringing up the network, launching daemons and restarting them if they die. On Ubuntu and Debian the init system is systemd. Init also has a standing duty as the adoptive parent of orphaned processes, collecting their exit statuses so they do not linger as zombies. A container normally has no init system at all: its PID 1 is the application itself, so nothing starts services for you and nothing reaps orphans unless you add a minimal init such as the one <code>docker run --init</code> provides. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "init system",
    "see": [
      "pid-1",
      "systemd",
      "daemon",
      "zombie-process",
      "orphan-process"
    ]
  },
  "systemd": {
    "name": "systemd",
    "short": "The init system and service manager on Ubuntu, Debian and most mainstream distributions; it starts services at boot, supervises them, and collects their logs.",
    "def": "systemd runs as PID 1 on a normal Ubuntu machine. It reads declarative unit files that say what to start, in what order and what to do on failure; you drive it with <code>systemctl</code> (<code>status</code>, <code>start</code>, <code>stop</code>, <code>enable</code>) and read what its services printed with <code>journalctl</code>. It exists so that services come up reliably and are restarted when they crash, without hand-written boot scripts. The catch for eval work is that containers almost never run systemd, so <code>systemctl start postgresql</code> inside a task container fails even though the package is installed. Agents burn turns on this, and task authors who developed on a VM ship setup scripts that silently do nothing in the container. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a>.",
    "also": "systemctl",
    "see": [
      "init",
      "unit",
      "journal",
      "daemon",
      "pid-1"
    ]
  },
  "unit": {
    "name": "Unit",
    "short": "A systemd configuration file describing one thing systemd manages, most commonly a service: what command to run, as which user, and when to restart it.",
    "def": "systemd manages the machine as a set of units, each defined by a small INI-style file. The kind you meet most is the service unit (<code>nginx.service</code>), which names the command to run, the user to run it as, what it depends on and the restart policy. Other types cover mounts, sockets and timers. Units shipped by packages live under <code>/usr/lib/systemd/system</code> and local ones under <code>/etc/systemd/system</code>; <code>systemctl cat name</code> prints the file and <code>systemctl list-units</code> shows what is loaded. On a VM-based sandbox the unit file is the authoritative answer to how a service was started and with what privileges and environment. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a>.",
    "also": "unit file, service unit",
    "see": [
      "systemd",
      "daemon",
      "journal",
      "service-account"
    ]
  },
  "journal": {
    "name": "Journal",
    "short": "systemd's central log store, which captures the output of every service plus kernel messages, and is read and filtered with journalctl.",
    "def": "On a systemd machine anything a service writes to stdout or stderr is captured by <code>journald</code> along with metadata — which unit, which PID, which boot, what time. You query it with <code>journalctl</code>: <code>-u nginx</code> for one unit, <code>-b</code> for the current boot, <code>-f</code> to follow, <code>-k</code> for kernel messages. The store is binary and indexed, which makes filtering fast but means you cannot simply <code>grep</code> a file. It exists so there is one place to look instead of a per-program scatter of log files. A container has no journal; the equivalent is whatever PID 1 wrote to its streams, which you read from outside with <code>docker logs</code>. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a>.",
    "also": "journald, journalctl",
    "see": [
      "systemd",
      "syslog",
      "dmesg",
      "unit",
      "stderr"
    ]
  },
  "syslog": {
    "name": "syslog",
    "short": "The traditional Unix logging system, in which programs send messages to a log daemon that writes them to plain-text files under /var/log.",
    "def": "Before the journal, and still alongside it on many machines, programs logged by sending messages to a syslog daemon such as <code>rsyslog</code>, which sorted them by source and severity into text files under <code>/var/log</code> — on Ubuntu the general-purpose one is <code>/var/log/syslog</code>. Because the files are plain text, everything from <a href='pages/05-text-fu.html'>Text-Fu</a> applies: <code>grep</code>, <code>tail -f</code>, <code>awk</code>. Containers typically run no syslog daemon, so <code>/var/log</code> there is nearly empty and a program that logs only to syslog is effectively silent. That is one reason container software is conventionally configured to log to stdout and stderr, where the harness can capture it. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a>.",
    "also": "rsyslog, /var/log/syslog",
    "see": [
      "journal",
      "dmesg",
      "daemon",
      "stdout"
    ]
  },
  "dmesg": {
    "name": "dmesg",
    "short": "The command that prints the kernel's own message log, where hardware events, driver messages and out-of-memory kills are recorded.",
    "def": "The kernel cannot use ordinary log files — it is running before any filesystem is mounted — so it writes messages into a fixed-size buffer in memory, and <code>dmesg</code> prints that buffer (<code>journalctl -k</code> shows the same thing on a systemd machine). It is where you find evidence that no user-space program can report: the OOM killer naming the process it killed, a disk returning errors, a filesystem being remounted read-only. Because containers share the host's kernel, this log belongs to the host; from inside a container reading it is normally refused with <code>Operation not permitted</code>, so confirming an out-of-memory kill is a job for the host or the harness. See <a href='pages/13-services-and-logs.html'>Services, Init, and Logs</a> and <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "kernel ring buffer, kernel log",
    "see": [
      "kernel",
      "oom-killer",
      "journal",
      "syslog"
    ]
  },
  "signal": {
    "name": "Signal",
    "short": "A small numbered notification the kernel delivers to a process, used to ask it to stop, force it to die, or tell it that something happened.",
    "def": "Signals are the kernel's way of interrupting a process from outside. Each has a name and a number — SIGINT 2, SIGKILL 9, SIGTERM 15 — and you send one with <code>kill -TERM 4312</code> (the <code>kill</code> command sends any signal, not only fatal ones). For most signals the target may install a handler and react however it likes — clean up, reload configuration, ignore it; without a handler a default action applies, usually termination. SIGKILL and SIGSTOP cannot be caught or ignored. A process ended by a signal has no exit code of its own, so the shell reports 128 plus the signal number: 137 means SIGKILL, 143 means SIGTERM. Reading those numbers tells you who ended an agent's command, and how. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a> and <a href='appendices/b-exit-codes-signals.html'>Appendix B</a>.",
    "see": [
      "sigterm",
      "sigkill",
      "sigint",
      "sighup",
      "exit-status"
    ]
  },
  "sigterm": {
    "name": "SIGTERM",
    "short": "Signal 15, the polite request to terminate: a process may catch it to clean up before exiting, and it is what kill and docker stop send first.",
    "def": "SIGTERM is the default signal sent by <code>kill</code>, by the <code>timeout</code> command and by <code>docker stop</code>. It asks rather than forces: a well-behaved program catches it, flushes files, closes connections and exits; a program with no handler is simply terminated. Because it can be caught, it can also be ignored, which is why every stop mechanism pairs it with a deadline and a SIGKILL. A process that dies from SIGTERM is reported by the shell as exit status 143 (128 + 15). If a harness stops containers with too short a grace period, partially written result files and half-flushed logs are the symptom. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a> and <a href='appendices/b-exit-codes-signals.html'>Appendix B</a>.",
    "also": "signal 15, exit 143",
    "see": [
      "signal",
      "sigkill",
      "timeout",
      "pid-1",
      "exit-status"
    ]
  },
  "sigkill": {
    "name": "SIGKILL",
    "short": "Signal 9, the unconditional kill: the kernel removes the process immediately, and the process cannot catch, block or ignore it.",
    "def": "SIGKILL is never delivered to the program at all — the kernel simply stops scheduling the process and tears it down. That makes it the one reliable way to end something that is hung or ignoring SIGTERM, and also means the program gets no chance to clean up: temporary files stay, buffered output is lost, child processes are left running as orphans. The shell reports such a death as exit status 137 (128 + 9). In sandboxes 137 has two common causes worth telling apart: a timeout that escalated to SIGKILL, and the kernel's OOM killer enforcing a memory limit. Neither is the model returning a wrong answer, so neither should be scored as one without a look. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a> and <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "signal 9, kill -9, exit 137",
    "see": [
      "signal",
      "sigterm",
      "oom-killer",
      "timeout",
      "infrastructure-failure"
    ]
  },
  "sigint": {
    "name": "SIGINT",
    "short": "Signal 2, the interrupt sent to the foreground program when you press Ctrl+C in a terminal.",
    "def": "Pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> does not send a character to your program; the terminal driver turns the keystroke into SIGINT and delivers it to the foreground process group. Most programs die on it (exit status 130, which is 128 + 2); interactive ones such as a Python REPL or a pager catch it and merely cancel the current action. The mechanism needs a terminal. An agent whose bash tool runs commands without a TTY has no <kbd>Ctrl</kbd>+<kbd>C</kbd> to press, so a hung command can only be ended by the harness's timeout; terminal-driven harnesses that type into tmux can send the keystroke, and you will see agents do exactly that in transcripts. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "signal 2, Ctrl+C, exit 130",
    "see": [
      "signal",
      "sigterm",
      "tty",
      "job-control",
      "tmux"
    ]
  },
  "sighup": {
    "name": "SIGHUP",
    "short": "Signal 1, the hang-up signal sent to a terminal's processes when that terminal closes; many daemons reuse it to mean reload your configuration.",
    "def": "SIGHUP dates from modems hanging up the phone line. Today it is sent to the processes attached to a terminal when that terminal goes away — you close the window, or an SSH connection drops — and its default action is to terminate them. That is why a long job started over SSH dies when your laptop sleeps, and why <code>nohup</code>, <code>tmux</code> and proper services exist: each keeps a job alive after the terminal that started it is gone. Daemons have no terminal to lose, so by convention many treat SIGHUP as a request to re-read their configuration. For multi-hour eval runs on a remote box, start them inside tmux rather than in a bare SSH session. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "signal 1, hang-up, nohup",
    "see": [
      "signal",
      "tty",
      "tmux",
      "ssh",
      "daemon"
    ]
  },
  "timeout": {
    "name": "Timeout",
    "short": "A limit on how long a command may run before it is killed; also the coreutils command that enforces one and exits with status 124 when the limit is hit.",
    "def": "Anything that can hang needs a deadline, and an agent's commands hang often: a program waiting for input, a server that never returns, a download with no route out. <code>timeout 60 cmd</code> runs <code>cmd</code>, sends SIGTERM after 60 seconds and exits with status 124; adding <code>-k 5</code> follows up with SIGKILL five seconds later if the program ignored the first signal. Harnesses apply the same pattern per tool call and per sample. Timeouts are measured in wall-clock time, so a slow or overloaded host turns into more timeouts and a lower score with no change in the model. A timed-out command also may leave children running. See <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a> and <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "exit 124, time limit",
    "see": [
      "sigterm",
      "sigkill",
      "wall-clock-time",
      "orphan-process",
      "infrastructure-failure"
    ]
  },
  "job-control": {
    "name": "Job Control",
    "short": "The interactive shell's feature for running several commands from one terminal: start one in the background, suspend the foreground one with Ctrl+Z, and resume either with fg or bg.",
    "def": "A terminal has one foreground at a time, so the shell lets you juggle. <code>cmd &amp;</code> starts a job in the background, <kbd>Ctrl</kbd>+<kbd>Z</kbd> suspends the foreground job, <code>jobs</code> lists them, and <code>fg</code> or <code>bg</code> resumes one in the foreground or background. Underneath, the shell places each job in its own process group and tells the terminal which group currently owns the keyboard. Job control is a feature of interactive shells; in scripts and in the non-interactive shells most harnesses use to run an agent's commands it is switched off, so <code>&amp;</code> still works but <code>fg</code> does not. For anything that must outlive one command, use tmux or a real service. See <a href='pages/09-processes.html'>Processes</a>.",
    "also": "jobs, fg, bg",
    "see": [
      "background-process",
      "sigint",
      "tty",
      "tmux",
      "shell"
    ]
  },
  "background-process": {
    "name": "Background Process",
    "short": "A process started so that the shell does not wait for it to finish, typically by ending the command with an ampersand, leaving it running while other commands execute.",
    "def": "Normally the shell starts a command and waits for it. Ending the command with <code>&amp;</code> skips the wait: the shell prints a job number and PID and returns at once while the process runs on. That is how you start a server and then talk to it from the same session, and agents do it constantly (<code>python app.py &amp;</code>). Two consequences follow. The process still holds the shell's stdout and stderr unless redirected, which can make a harness wait for output that never ends. And it may outlive the command that launched it, so it is still there — holding a port, using memory — when later commands and the scorer run. See <a href='pages/09-processes.html'>Processes</a>.",
    "also": "background job",
    "see": [
      "job-control",
      "orphan-process",
      "daemon",
      "process",
      "listening-socket"
    ]
  },
  "environment-variable": {
    "name": "Environment Variable",
    "short": "A named string attached to a process and copied to every process it starts, used to pass configuration such as PATH, HOME or an API key.",
    "def": "Every process carries a list of <code>NAME=value</code> strings called its environment. A child receives a copy of its parent's environment when it is created, which is what makes it a configuration channel: set a variable once in the shell, <code>export</code> it, and every program started from that shell sees it. Copies flow one way only — a child cannot change its parent's environment, which is why running a script cannot alter your shell's variables but sourcing it can. Inspect the environment with <code>env</code> or <code>printenv</code>, or read another process's from <code>/proc/PID/environ</code>. In a sandbox, whatever the harness placed in the container's environment is readable by the agent with a single command. See <a href='pages/11-environment-and-secrets.html'>Environment Variables and Secrets</a>.",
    "also": "env var, environment",
    "see": [
      "path-variable",
      "secret",
      "parent-process",
      "fork-exec",
      "proc-filesystem"
    ]
  },
  "secret": {
    "name": "Secret",
    "short": "Any credential that grants access, such as an API key, token, password or private key, and which must not be readable by the thing being evaluated.",
    "def": "Eval infrastructure runs on secrets: model-provider API keys, registry tokens, cloud credentials, SSH keys. The common way to hand one to a program is an environment variable, and that is also the common way to leak one. Environment variables are inherited by every child process, are readable from <code>/proc/PID/environ</code> by the same user and by root, appear in <code>docker inspect</code> output, and end up in a transcript the moment an agent runs <code>env</code>. The working rule is that anything inside the sandbox — environment, mounted files, image layers, shell history — is visible to the agent, so credentials the harness needs stay with the harness, outside the box. See <a href='pages/11-environment-and-secrets.html'>Environment Variables and Secrets</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "credential, API key, token",
    "see": [
      "environment-variable",
      "least-privilege",
      "metadata-service",
      "trust-boundary",
      "solution-leakage"
    ]
  },
  "load-average": {
    "name": "Load Average",
    "short": "Three numbers reporting how many processes were running or waiting to run, averaged over the last 1, 5 and 15 minutes; compare them with the CPU count.",
    "def": "<code>uptime</code> and <code>top</code> print three load averages: the average number of processes that were runnable — on a CPU or queued for one — over the past one, five and fifteen minutes. Linux also counts processes stuck in uninterruptible waits, usually on disk, so heavy I/O raises the figure too. The number only means something next to the CPU count from <code>nproc</code>: a load of 8 on sixteen cores is comfortable, on two cores it is a queue. Inside a container the figure describes the whole host, not your container. It is the quickest check when tasks start timing out: if load far exceeds cores, the box is oversubscribed and the clock, not the model, is failing samples. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "see": [
      "cpu-time",
      "wall-clock-time",
      "timeout",
      "cgroup",
      "flaky-test"
    ]
  },
  "oom-killer": {
    "name": "OOM Killer",
    "short": "The kernel mechanism that, when memory runs out on the machine or within a container's limit, picks a process and kills it with SIGKILL.",
    "def": "Linux lets processes reserve more memory than exists, betting they will not all use it. When the bet fails — the machine, or a cgroup with a memory limit, genuinely runs out — the kernel cannot return an error to anyone in particular, so it chooses a victim, usually the largest consumer, and sends SIGKILL. The victim gets no warning and prints no message; its parent sees exit status 137 and the shell may print <code>Killed</code>. The evidence lives elsewhere: in the kernel log, and for Docker containers in the <code>OOMKilled</code> field of <code>docker inspect</code>. A task whose tests need more memory than the sandbox allows fails this way for every model, which is an infrastructure failure to fix, not a score to report. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "out-of-memory killer, OOM",
    "see": [
      "sigkill",
      "memory-rss",
      "cgroup",
      "dmesg",
      "infrastructure-failure"
    ]
  },
  "rlimit": {
    "name": "Resource Limit (rlimit)",
    "short": "A per-process cap set through the kernel, for example on open files, process count or file size, inherited by child processes and viewed with ulimit.",
    "def": "Resource limits are the older, per-process way of stopping one program from exhausting a machine. Each limit — open file descriptors, number of processes for the user, largest file size, stack size, CPU seconds — has a soft value that is enforced and a hard ceiling that the soft value may be raised to. Children inherit them, so a limit set in a shell with <code>ulimit</code> applies to everything launched from it; <code>ulimit -a</code> lists the current values. Hitting one produces an ordinary error such as <code>Too many open files</code>, rather than a kill. Containers rely mainly on cgroups, which cap a whole group of processes instead of each one, but rlimits still apply inside and differ between hosts. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "ulimit, setrlimit",
    "see": [
      "cgroup",
      "file-descriptor",
      "oom-killer",
      "process"
    ]
  },
  "nice": {
    "name": "nice",
    "short": "A process's scheduling priority hint, from -20 (most favoured) to 19 (least); the nice command starts a program with a lowered priority.",
    "def": "When more processes want the CPU than there are cores, the scheduler must choose, and the nice value tilts that choice. It runs from -20 to 19 with a default of 0, and the name is literal: a higher number is nicer to everyone else and receives a smaller share. <code>nice -n 10 cmd</code> starts a command at lower priority and <code>renice</code> changes a running one; only root may make a process less nice. It has no effect on an idle machine and is no limit at all — a niced process will still use every idle core. To cap CPU for a sandbox you want a cgroup limit such as Docker's <code>--cpus</code>. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "niceness, renice",
    "see": [
      "cpu-time",
      "load-average",
      "cgroup",
      "process"
    ]
  },
  "cpu-time": {
    "name": "CPU Time",
    "short": "The amount of time a processor actually spent executing a process's instructions, as opposed to how long the process took by the clock.",
    "def": "The kernel accounts for each process's time on a CPU, split into user time (running the program's own code) and system time (the kernel working on its behalf). <code>time cmd</code> prints both beside <code>real</code>, the elapsed time. Comparing them is diagnostic: CPU time close to real means the program was computing; CPU time far below real means it was waiting — on disk, the network, a lock, or for a turn on a contended or throttled CPU; CPU time above real means several cores ran in parallel. A container with a CPU cap is throttled once it uses its share, so the same test suite does the same CPU work but takes longer by the clock. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "user time, system time",
    "see": [
      "wall-clock-time",
      "load-average",
      "cgroup",
      "nice",
      "timeout"
    ]
  },
  "wall-clock-time": {
    "name": "Wall-Clock Time",
    "short": "Elapsed real-world time between a command starting and finishing, as a clock on the wall would measure it, including all waiting.",
    "def": "Wall-clock time is what <code>time</code> reports as <code>real</code>: start to finish, including every moment the process spent waiting rather than computing. It is what users feel and what almost every timeout measures, and it depends on much more than the program: how many other containers share the host, CPU throttling, a cold disk cache, network latency, a package mirror having a bad day. For evals this makes it the noisy variable. Two runs of the same agent on the same task can land on opposite sides of a timeout purely because of what else the host was doing, so record durations, set limits with headroom, and treat clusters of timeouts as a host problem first. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "real time, elapsed time",
    "see": [
      "cpu-time",
      "timeout",
      "load-average",
      "nondeterminism",
      "flaky-test"
    ]
  },
  "memory-rss": {
    "name": "Resident Set Size (RSS)",
    "short": "The amount of physical RAM a process currently occupies, as opposed to the usually much larger amount of address space it has reserved.",
    "def": "<code>ps</code> and <code>top</code> show two memory columns per process. VSZ (virtual size) is all the address space the process has mapped, much of it never touched; RSS is the part actually sitting in physical RAM right now, and it is the one that tells you who is using the memory. Even RSS is approximate: pages shared between processes, such as common libraries, are counted once for each, so adding up RSS overstates the total. A container's memory limit is enforced on the cgroup's accounting, which also includes file cache charged to the group, so the figure to compare with the limit is the cgroup's own counter rather than a sum over <code>ps</code>. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "RSS, RES, resident memory",
    "see": [
      "oom-killer",
      "swap",
      "cgroup",
      "process"
    ]
  },
  "swap": {
    "name": "Swap",
    "short": "Disk space the kernel uses as overflow for RAM, moving idle memory pages out to disk so that the machine slows down instead of running out of memory.",
    "def": "When physical memory fills, the kernel can write pages that have not been used recently to a swap partition or file and reuse the RAM, reading them back when they are next touched. It turns a hard failure into a soft one — but disk is vastly slower than RAM, so a machine that is actively swapping keeps working at a crawl. <code>free -h</code> shows how much swap exists and how much is in use. For evals, swap converts memory pressure from a clear signal (an OOM kill, exit 137) into an ambiguous one (everything becomes slow and timeouts fire). Whether a container may use swap depends on host and runtime settings, so the same task image can behave differently on two hosts. See <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "swap space, paging",
    "see": [
      "memory-rss",
      "oom-killer",
      "wall-clock-time",
      "cgroup"
    ]
  },
  "kernel": {
    "name": "Kernel",
    "short": "The core program of the operating system: it alone controls the hardware and decides what every process may do with CPU, memory, files and the network.",
    "def": "Linux, strictly speaking, is the kernel: the one program that runs with full control of the hardware. It schedules processes onto CPUs, hands out memory, implements filesystems and the network stack, and enforces permissions. Everything else — the shell, Python, your agent — is an ordinary process that must ask the kernel for anything involving the outside world. The fact that shapes this course is that containers do not have a kernel of their own; every container on a host shares the host's. <code>uname -r</code> inside a container prints the host's kernel version (on a Mac, that of Docker's hidden Linux VM). A shared kernel is what makes containers cheap, and it is why a kernel bug is a route out of one. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "Linux kernel",
    "see": [
      "system-call",
      "user-space",
      "namespace",
      "container",
      "virtual-machine"
    ]
  },
  "system-call": {
    "name": "System Call",
    "short": "A request from a process to the kernel to do something the process cannot do itself, such as open a file, start a process, or send data over the network.",
    "def": "A process can compute inside its own memory unaided, but touching anything shared — files, the network, other processes, the clock — requires asking the kernel through a system call. There are a few hundred, with names you will recognise from error messages and traces: <code>openat</code>, <code>read</code>, <code>write</code>, <code>execve</code>, <code>connect</code>, <code>mount</code>. When a call fails the kernel returns an error code such as <code>ENOENT</code> or <code>EACCES</code>, which the program turns into messages like No such file or directory or Permission denied. Since every meaningful action crosses this one interface, it is where sandboxes are enforced: seccomp filters which calls a container may make, and gVisor intercepts them entirely. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a> and <a href='pages/20-namespaces.html'>Namespaces</a>.",
    "also": "syscall",
    "see": [
      "kernel",
      "user-space",
      "seccomp",
      "strace",
      "gvisor"
    ]
  },
  "user-space": {
    "name": "User Space",
    "short": "Everything that runs outside the kernel: ordinary programs, libraries, shells and services, which reach hardware only by making system calls.",
    "def": "The CPU runs code in two modes. Kernel mode can do anything; user mode cannot touch hardware or other processes' memory directly. User space is all the code running in the second mode — the shell, coreutils, the C library, Python, databases, your agent's tools. The split exists for protection: a bug in a user-space program kills that program, while a bug in the kernel can take down or compromise the machine. It also pins down what a container image is: a bundle of user-space files, and nothing more. An Ubuntu image running on another distribution's kernel is Ubuntu's user space talking to that kernel, which works because the system-call interface is kept stable. See <a href='pages/20-namespaces.html'>Namespaces</a>.",
    "also": "userland, user mode",
    "see": [
      "kernel",
      "system-call",
      "distribution",
      "image",
      "musl-glibc"
    ]
  },
  "strace": {
    "name": "strace",
    "short": "A debugging tool that prints every system call a program makes, with arguments and results, showing what the program actually asked the kernel to do.",
    "def": "When a program fails with an unhelpful message, <code>strace</code> shows the ground truth: each system call, its arguments and what the kernel answered. <code>strace -f -e trace=openat,execve cmd</code> follows child processes and shows only file opens and program launches, which is usually enough to see which configuration file it looked for, in which directories, and which one came back <code>ENOENT</code>. Attach to a running process with <code>-p PID</code> to see what a hung one is blocked on. It is not installed in most images, slows the traced program considerably, and depends on the ptrace facility, which a container's seccomp profile or capability set may deny. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a> and <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a>.",
    "see": [
      "system-call",
      "kernel",
      "seccomp",
      "capability",
      "process"
    ]
  },
  "package-manager": {
    "name": "Package Manager",
    "short": "The tool that installs, upgrades and removes software on a system, fetching packages from repositories and working out which other packages each one needs.",
    "def": "On Linux you rarely download an installer. A package manager fetches a named package from a repository, verifies it, works out and installs everything it depends on, unpacks the files into the right directories and records what it did so the package can later be upgraded or removed cleanly. Each ecosystem has its own: <code>apt</code> on Debian and Ubuntu, <code>apk</code> on Alpine, <code>pip</code> for Python libraries. The convenience has a cost for evals: <code>install X</code> means the newest X the repository offers today, so the same build script produces different environments in different months unless versions are pinned. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "see": [
      "apt",
      "dpkg",
      "pip",
      "repository",
      "dependency"
    ]
  },
  "apt": {
    "name": "apt",
    "short": "The package manager for Debian and Ubuntu: it downloads packages and their dependencies from configured repositories and hands them to dpkg to install.",
    "def": "APT is the high-level package tool on Debian-family systems. <code>apt-get update</code> downloads the repositories' current package indexes; <code>apt-get install -y name</code> resolves dependencies, downloads the <code>.deb</code> files and has dpkg install them. Use <code>apt-get</code> in scripts and Dockerfiles: the friendlier <code>apt</code> command warns that its interface is not stable for scripting. Official Docker images ship with no indexes, so an install before any <code>update</code> fails with <code>Unable to locate package</code> — one of the most common errors in agent transcripts. Two others: a confirmation or configuration prompt that hangs a non-interactive session (use <code>-y</code> and <code>DEBIAN_FRONTEND=noninteractive</code>), and the lock error when two installs run at once. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "apt-get, APT",
    "see": [
      "dpkg",
      "package-manager",
      "repository",
      "version-pinning",
      "interactive-prompt"
    ]
  },
  "dpkg": {
    "name": "dpkg",
    "short": "The low-level Debian package tool that actually unpacks .deb files and keeps the database of which packages and files are installed.",
    "def": "apt decides what to install; dpkg does the installing. It unpacks a <code>.deb</code> archive, runs the package's setup scripts and records every file in a database under <code>/var/lib/dpkg</code>. It knows nothing about repositories or dependency resolution, which is why you seldom install with it directly, but it is the tool for questions about what is already on a box: <code>dpkg -l</code> lists installed packages with versions, <code>dpkg -L pkg</code> lists a package's files, and <code>dpkg -S /path</code> names the package that owns a file. Saving <code>dpkg -l</code> output from a task image gives you an inventory to diff against the next rebuild, which is how you catch environment drift. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": ".deb",
    "see": [
      "apt",
      "package-manager",
      "debian",
      "reproducible-build"
    ]
  },
  "repository": {
    "name": "Repository (Package)",
    "short": "A server holding packages and a signed index of them, which a package manager consults to find, download and verify software.",
    "def": "A package repository is a published collection of packages plus an index listing names, versions, dependencies and checksums, signed so that clients can detect tampering. A machine's list of repositories is configuration: for apt it lives under <code>/etc/apt/sources.list.d/</code> (Ubuntu 24.04 uses <code>ubuntu.sources</code>), and for pip the default is the Python Package Index. Repositories are living things — new versions appear and old ones are removed — so the same install command returns different software over time. They are also a network dependency: a sandbox with no egress cannot install anything, so whatever a task needs must be baked into the image or served from a mirror you control. (A git repository is an unrelated use of the word.) See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "repo, package archive, mirror",
    "see": [
      "apt",
      "package-manager",
      "registry",
      "egress",
      "version-pinning"
    ]
  },
  "dependency": {
    "name": "Dependency",
    "short": "Another package that a piece of software needs in order to work; dependencies have dependencies of their own, forming a tree the package manager resolves.",
    "def": "Almost no software stands alone. A package declares what it needs — a library, an interpreter, another tool — often with a version range, and the package manager installs those too, and then what they need in turn. The ones you asked for are direct dependencies; the rest are transitive, and there are usually far more of them. That is where reproducibility goes wrong: you pin the three libraries you know about, and an unpinned transitive dependency releases a new version that changes behaviour or breaks the build. For a benchmark this shows up as a task whose tests passed last quarter and now fail for every model, with no change to the task. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "transitive dependency",
    "see": [
      "package-manager",
      "version-pinning",
      "lockfile",
      "reproducible-build"
    ]
  },
  "version-pinning": {
    "name": "Version Pinning",
    "short": "Specifying the exact version of a package to install instead of whatever is newest, so that an environment built later matches one built today.",
    "def": "Without a pin, an install command means the latest version as of now. Pinning replaces that with an exact version: <code>pip install requests==2.32.3</code>, <code>apt-get install curl=VERSION</code>, or a base image named by digest rather than by tag. It exists because an eval environment is a measuring instrument and an instrument should not change between measurements. Two limits are worth knowing. Pinning only your direct dependencies leaves the transitive ones floating, which is the job of a lockfile. And distribution repositories usually keep only current versions, so an apt pin can stop resolving months later; building against a dated snapshot of the archive is the durable fix. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "pinning, pin",
    "see": [
      "lockfile",
      "dependency",
      "image-digest",
      "reproducible-build",
      "nondeterminism"
    ]
  },
  "lockfile": {
    "name": "Lockfile",
    "short": "A generated file recording the exact version, and usually a checksum, of every direct and transitive dependency, so an install can be repeated exactly.",
    "def": "A requirements file says what you want (<code>pandas&gt;=2</code>); a lockfile records what you got — every package in the resolved tree, each at one exact version, ideally with a hash of the downloaded file. Installing from the lockfile skips resolution and reproduces that set, and with hashes it refuses anything that does not match (pip's <code>--require-hashes</code> mode). Examples are a fully pinned <code>requirements.txt</code> produced by a lock tool, <code>uv.lock</code>, <code>poetry.lock</code> and <code>package-lock.json</code>. Commit the lockfile beside the task's Dockerfile. It covers one ecosystem only: system packages and the base image need pinning of their own. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "lock file",
    "see": [
      "version-pinning",
      "dependency",
      "pip",
      "reproducible-build",
      "image-digest"
    ]
  },
  "reproducible-build": {
    "name": "Reproducible Build",
    "short": "A build process that yields the same result every time it runs on the same inputs, regardless of when or where it is run.",
    "def": "In the strict sense a reproducible build is bit-for-bit identical on every run. Eval work usually needs the practical version: rebuild the task image next year and get the same software at the same versions behaving the same way. A plain Dockerfile is not reproducible by default. <code>FROM ubuntu:24.04</code> names a tag that is updated in place, <code>apt-get update</code> reads today's index, and <code>pip install</code> resolves today's newest releases. The remedies stack up: pin the base image by digest, pin or snapshot system packages, install language packages from a lockfile — and then push the built image to a registry and run it by digest, so you rarely rebuild at all. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "also": "reproducibility, environment drift",
    "see": [
      "version-pinning",
      "lockfile",
      "base-image",
      "image-digest",
      "nondeterminism"
    ]
  },
  "base-image": {
    "name": "Base Image",
    "short": "The existing container image a Dockerfile starts from, named on its FROM line, which supplies the distribution's files underneath everything you add.",
    "def": "Nobody builds a container image from nothing. The <code>FROM</code> line of a Dockerfile picks a base — <code>ubuntu:24.04</code>, <code>debian:bookworm-slim</code>, <code>python:3.12-slim</code>, <code>alpine:3.20</code> — and every later instruction adds layers on top. The choice fixes more than it seems to: the package manager, the C library, the shell, which everyday tools exist, and how large the image is. Official bases are deliberately minimal, so expect no <code>curl</code>, no <code>ping</code> and no <code>python3</code> in <code>ubuntu:24.04</code> until you install them. A base named by tag also changes underneath you as its publisher rebuilds it, so pin it by digest for anything you intend to measure with. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "parent image, FROM",
    "see": [
      "image",
      "dockerfile",
      "image-digest",
      "tag",
      "distribution"
    ]
  },
  "distribution": {
    "name": "Distribution",
    "short": "A complete operating system assembled around the Linux kernel: a chosen set of user-space tools, a package manager, default settings and a release schedule.",
    "def": "Linux itself is only a kernel. A distribution — Ubuntu, Debian, Alpine, Fedora — combines it with a C library, a shell, core utilities, an init system and a package manager, and publishes tested releases of the whole. Distributions differ exactly where it hurts in a transcript: which package manager exists (<code>apt</code> or <code>apk</code>), what packages are called, whether <code>bash</code> is present, where configuration lives. A container image carries a distribution's user space but none of its kernel, so the distribution inside a container can differ from the host's. The first command on an unfamiliar box is <code>cat /etc/os-release</code>, which tells you which one you are in and therefore which commands will work. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/00-orientation.html'>Orientation</a>.",
    "also": "distro",
    "see": [
      "debian",
      "ubuntu",
      "alpine",
      "user-space",
      "package-manager"
    ]
  },
  "debian": {
    "name": "Debian",
    "short": "A long-established community Linux distribution known for stability; it is the parent of Ubuntu and the base of many official Docker images.",
    "def": "Debian is a community-run distribution whose stable releases change slowly and carefully; the current one used in this course is Debian 12, codenamed bookworm. It originated the <code>.deb</code> package format and the apt and dpkg tools, so nearly everything the course teaches on Ubuntu applies unchanged. You meet Debian most often without choosing it: many official language images on Docker Hub, including the default <code>python</code> images, are built on it, and <code>debian:bookworm-slim</code> is a popular small base. Image tags carry the codename (<code>python:3.12-slim-bookworm</code>), which is how you tell which Debian release, and so which package versions, a task image sits on. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "bookworm",
    "see": [
      "ubuntu",
      "distribution",
      "apt",
      "dpkg",
      "base-image"
    ]
  },
  "ubuntu": {
    "name": "Ubuntu",
    "short": "A widely used Linux distribution derived from Debian, with long-term-support releases every two years; Ubuntu 24.04 LTS is this course's reference system.",
    "def": "Ubuntu is built from Debian by Canonical and shares its tooling: apt, dpkg, <code>.deb</code> packages, systemd. Versions are named by year and month, so 24.04 is the April 2024 release (codename noble), and the April release of every even year is a long-term-support (LTS) version maintained for years — the ones servers, cloud VMs and task images are built on. The Docker image <code>ubuntu:24.04</code> is much smaller than an installed Ubuntu machine: there is no systemd running, and everyday tools such as <code>curl</code>, <code>ping</code> and <code>python3</code> are absent until installed. Expecting the VM experience inside the container is a routine source of confusion for people and agents alike. See <a href='pages/01-lab-setup.html'>Lab Setup</a> and <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "Ubuntu LTS, noble",
    "see": [
      "debian",
      "distribution",
      "apt",
      "systemd",
      "base-image"
    ]
  },
  "alpine": {
    "name": "Alpine Linux",
    "short": "A very small Linux distribution popular for container images; it uses musl instead of glibc, BusyBox instead of GNU tools, and apk instead of apt.",
    "def": "Alpine's base image is a small fraction of the size of Ubuntu's, which is why so many container images build on it. It gets there by swapping out the usual parts: the musl C library instead of glibc, a single BusyBox binary standing in for the GNU core utilities, <code>apk add</code> instead of <code>apt-get install</code>, and the BusyBox <code>ash</code> shell at <code>/bin/sh</code>, with no bash unless you add it. Each swap is a trap for habits formed on Ubuntu: scripts with a <code>#!/bin/bash</code> line will not start, familiar GNU flags are missing, and software compiled for glibc will not run. An agent that assumes Ubuntu inside an Alpine task image loses several turns finding this out. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "apk",
    "see": [
      "musl-glibc",
      "busybox",
      "distribution",
      "base-image",
      "gnu-coreutils"
    ]
  },
  "musl-glibc": {
    "name": "musl vs glibc",
    "short": "The two common C standard libraries on Linux: glibc on Ubuntu, Debian and most distributions, musl on Alpine; programs built for one generally will not run on the other.",
    "def": "Nearly every program reaches the kernel through a C library, which wraps system calls and supplies basics such as memory allocation and name resolution. Mainstream distributions use GNU libc (glibc); Alpine uses musl, which is smaller and simpler. A dynamically linked binary names the specific loader and library it was built against, so a glibc-built program copied into Alpine fails — often with a baffling <code>not found</code> for a file that plainly exists, because the missing thing is the loader, not the program. For Python, prebuilt wheels are published per C library: if a package has no musl wheel, pip falls back to compiling from source, needing compilers the image lacks. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "libc, C library",
    "see": [
      "alpine",
      "user-space",
      "system-call",
      "pip",
      "distribution"
    ]
  },
  "pip": {
    "name": "pip",
    "short": "Python's package installer, which downloads libraries from the Python Package Index (PyPI) along with their dependencies.",
    "def": "<code>pip install name</code> fetches a library and whatever it depends on from PyPI into the current Python environment. It resolves versions at install time, so an unpinned install is a moving target; for reproducible task images install from a fully pinned requirements file, ideally with <code>--require-hashes</code>. Two behaviours fill transcripts. On Ubuntu 24.04 and Debian 12, running pip against the system Python is refused with <code>error: externally-managed-environment</code>, because the distribution's own tools depend on those packages — the intended answer is a virtual environment. And pip needs network access to PyPI, so in a sandbox with no egress every install fails, and tasks must ship their dependencies preinstalled. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "PyPI, pip install",
    "see": [
      "virtual-environment",
      "lockfile",
      "version-pinning",
      "package-manager",
      "egress"
    ]
  },
  "virtual-environment": {
    "name": "Virtual Environment",
    "short": "A self-contained directory holding its own Python packages, so that one project's libraries do not conflict with another's or with the system's.",
    "def": "<code>python3 -m venv .venv</code> creates a directory with its own <code>bin/python</code>, its own <code>pip</code> and its own package folder; whatever you install with that pip stays inside. It exists because one machine-wide set of packages cannot satisfy two projects that need different versions, and because the system Python's packages belong to the distribution. On Ubuntu the feature lives in a separate package, <code>python3-venv</code>. Activation is less magical than it looks: <code>source .venv/bin/activate</code> mostly puts the environment's <code>bin</code> directory first on <code>PATH</code> for the current shell. When a harness runs each command in a fresh shell, that activation is gone by the next command, so call <code>.venv/bin/python</code> by path instead. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "also": "venv, virtualenv",
    "see": [
      "pip",
      "path-variable",
      "lockfile",
      "dependency",
      "bash-tool"
    ]
  },
  "ip-address": {
    "name": "IP Address",
    "short": "The numeric address that identifies a network interface so that packets can be delivered to it, such as 172.17.0.2.",
    "def": "Every packet on an IP network carries a source and a destination address, and routers use the destination to move it hop by hop. Addresses belong to network interfaces rather than to machines, so one box commonly has several: <code>127.0.0.1</code> on loopback, a private address on its main interface, perhaps more on bridges. <code>ip addr</code> lists them; <code>hostname -I</code> prints just the addresses. A container gets an address of its own on a virtual network inside the host, distinct from the host's address, which is why a service in a container cannot be reached at the host's address until a port is published. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "IP",
    "see": [
      "ipv4",
      "ipv6",
      "cidr",
      "network-interface",
      "private-address-range"
    ]
  },
  "ipv4": {
    "name": "IPv4",
    "short": "The original and still dominant version of the Internet Protocol, with 32-bit addresses written as four decimal numbers from 0 to 255, such as 192.168.1.10.",
    "def": "An IPv4 address is 32 bits, written as four bytes in decimal separated by dots. Thirty-two bits allow about 4.3 billion addresses, far fewer than there are devices, and that shortage explains two things you meet everywhere: private address ranges that are reused inside every organisation, home and Docker host, and NAT, which lets many privately addressed machines share one public address. Almost all container networking you will inspect is IPv4 — Docker's default networks are IPv4-only unless configured otherwise. The dotted form hides the bit structure that subnet sizes depend on; <a href='appendices/c-binary-octal-cidr.html'>Appendix C</a> covers that arithmetic. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "see": [
      "ip-address",
      "ipv6",
      "cidr",
      "private-address-range",
      "nat"
    ]
  },
  "ipv6": {
    "name": "IPv6",
    "short": "The newer version of the Internet Protocol, with 128-bit addresses written in hexadecimal groups separated by colons, such as 2001:db8::1.",
    "def": "IPv6 was designed to end the address shortage: 128-bit addresses, written as up to eight groups of hexadecimal digits, with <code>::</code> standing for a run of zeros. Its loopback address is <code>::1</code>. Most machines run both protocols side by side, and that dual stack is the thing to watch. Firewall rules written for IPv4 do nothing to IPv6 traffic — with the older tools it is a separate ruleset — so an egress block can be complete for one protocol and absent for the other. A quieter surprise is <code>localhost</code> resolving to <code>::1</code> while a service listens only on <code>127.0.0.1</code>, giving connection refused for something that is plainly running. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "see": [
      "ipv4",
      "ip-address",
      "localhost",
      "firewall",
      "egress"
    ]
  },
  "cidr": {
    "name": "CIDR Notation",
    "short": "A compact way of writing a block of IP addresses as an address plus a prefix length, such as 10.0.0.0/8, where the number says how many leading bits are fixed.",
    "def": "<code>192.168.1.0/24</code> means the first 24 bits are fixed and the remaining 8 vary, so the block covers 192.168.1.0 through 192.168.1.255 — 256 addresses. Each bit removed from the prefix doubles the block: a <code>/16</code> holds 65,536 addresses, a <code>/8</code> about 16.7 million, and a <code>/32</code> is exactly one. The notation appears wherever a set of addresses is named: on interfaces (<code>172.17.0.2/16</code>), in routing tables, in firewall rules and in allowlists. Reading it correctly matters in an audit. A rule permitting <code>10.0.0.0/8</code> when <code>10.0.0.8/32</code> was intended opens the whole range rather than one host. <a href='appendices/c-binary-octal-cidr.html'>Appendix C</a> does the arithmetic; see also <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "prefix length, /24, netmask",
    "see": [
      "subnet",
      "ip-address",
      "ipv4",
      "private-address-range",
      "allowlist"
    ]
  },
  "subnet": {
    "name": "Subnet",
    "short": "A block of IP addresses that share a prefix and sit on one local network, so that their members can reach each other directly without passing through a router.",
    "def": "An interface's address comes with a prefix length, and together they define its subnet: <code>172.17.0.2/16</code> says everything in 172.17.x.x is a neighbour. When sending, the kernel asks one question — is the destination inside one of my subnets? If so the packet goes straight out of that interface; if not it goes to a gateway to be forwarded. That single test is why a wrong prefix produces strange partial connectivity. For sandboxes the subnet defines who the neighbours are. Containers attached to the same Docker network share a subnet and can reach each other directly, so two concurrently running samples placed on one network are not isolated from one another. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='appendices/c-binary-octal-cidr.html'>Appendix C</a>.",
    "also": "subnetwork, network prefix",
    "see": [
      "cidr",
      "routing-table",
      "default-gateway",
      "bridge-network",
      "ip-address"
    ]
  },
  "private-address-range": {
    "name": "Private Address Range",
    "short": "IPv4 blocks reserved for internal networks and never routed on the public internet: 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16.",
    "def": "RFC 1918 set aside three blocks that anyone may use internally without coordination — <code>10.0.0.0/8</code>, <code>172.16.0.0/12</code> and <code>192.168.0.0/16</code> — on the understanding that internet routers will not carry them. Reuse is the point: your home network, your employer's and every Docker host can all use the same numbers, reaching the outside through NAT. Docker's default bridge network is typically <code>172.17.0.0/16</code>, inside the second block. The audit consequence is that an address starting 10., 172.16–31. or 192.168. is not the internet but is somewhere: the host, a sibling container, a service on the internal network. Blocking internet access and blocking private ranges are separate decisions, and a sandbox usually needs both. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "RFC 1918, private IP",
    "see": [
      "cidr",
      "nat",
      "ipv4",
      "bridge-network",
      "metadata-service"
    ]
  },
  "network-interface": {
    "name": "Network Interface",
    "short": "A network attachment point as the kernel sees it, which may be a physical card or a purely virtual device, each with a name such as lo or eth0 and its own addresses.",
    "def": "The kernel sends and receives packets through interfaces. Some correspond to hardware, such as an Ethernet or Wi-Fi card; many are software only: <code>lo</code> for loopback, bridges, the virtual Ethernet pairs that wire up containers, VPN tunnels. <code>ip addr</code> lists each interface with its state and addresses, and <code>ip link</code> shows just the devices. A typical Docker container has exactly two, <code>lo</code> and <code>eth0</code>; one started with <code>--network none</code> has only <code>lo</code>, and that listing is the fastest proof that a no-network sandbox really has no network. Minimal images often lack the <code>ip</code> command, which comes from the <code>iproute2</code> package. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "NIC, interface, eth0",
    "see": [
      "ip-address",
      "loopback",
      "veth",
      "bridge-network",
      "network-namespace"
    ]
  },
  "loopback": {
    "name": "Loopback",
    "short": "A virtual network interface, named lo, that delivers traffic back to the same machine; addresses in 127.0.0.0/8, usually 127.0.0.1, never leave the box.",
    "def": "The loopback interface lets programs on one machine talk to each other with ordinary network code and no network: a test suite connecting to a local database, a browser to a development server. Anything sent to <code>127.0.0.1</code> (or <code>::1</code> in IPv6) is handed straight back by the kernel and never touches a wire. The subtlety in containers is that loopback belongs to a network namespace, so each container has its own private <code>lo</code>. A service listening on 127.0.0.1 inside a container is reachable only from inside that container — not from the host, not from a sibling container, and not through a published port. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "lo, 127.0.0.1",
    "see": [
      "localhost",
      "network-interface",
      "bind-address",
      "network-namespace"
    ]
  },
  "localhost": {
    "name": "localhost",
    "short": "The conventional hostname for this same machine, which resolves to the loopback address 127.0.0.1 (or ::1 for IPv6).",
    "def": "<code>localhost</code> is just a name, mapped to the loopback addresses by the first lines of <code>/etc/hosts</code>. It always means whichever network namespace the program is running in, and that is the trap once containers are involved. Inside a container, localhost is the container; a database running on your Mac or in another container is not there, however natural <code>localhost:5432</code> feels. In a multi-container task each service is reached by its service name on the shared network instead. A large share of connection refused errors in agent transcripts are this mistake, made either by the agent or by the task author who wrote the instructions. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a> and <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "see": [
      "loopback",
      "hosts-file",
      "bind-address",
      "network-namespace",
      "docker-compose"
    ]
  },
  "routing-table": {
    "name": "Routing Table",
    "short": "The kernel's list of rules for deciding, for each outgoing packet, which interface to send it out of and which next hop should receive it.",
    "def": "<code>ip route</code> prints the table. Each line pairs a destination block with a way to reach it: <code>172.17.0.0/16 dev eth0</code> means those addresses are directly attached, and <code>default via 172.17.0.1 dev eth0</code> means everything else is handed to that gateway. When several lines match, the most specific — the longest prefix — wins, with the default route as the fallback. The table is the definitive answer to where a box can send traffic. No default route means nothing beyond the local subnets is reachable, and the error is an immediate <code>Network is unreachable</code> rather than a timeout. It shows where packets may be sent, not whether a firewall further along lets them through. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "route, ip route",
    "see": [
      "default-gateway",
      "subnet",
      "cidr",
      "network-interface",
      "egress"
    ]
  },
  "default-gateway": {
    "name": "Default Gateway",
    "short": "The router a machine sends packets to when the destination is not on any directly attached network; it is the way out to everything else.",
    "def": "A machine knows how to reach its own subnets directly. For every other destination it needs a neighbour willing to forward packets, and the default route names that neighbour: <code>default via 172.17.0.1 dev eth0</code>. At home the gateway is your router. For a container on Docker's bridge network it is the host's end of the bridge, which leads to two facts worth remembering in an audit. All of the container's outside traffic passes through the host, where it can be filtered, logged or blocked. And the gateway address is the host itself as seen from inside the sandbox, so any service the host exposes on that address is reachable by the agent. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "gateway, default route",
    "see": [
      "routing-table",
      "subnet",
      "nat",
      "bridge-network",
      "egress"
    ]
  },
  "nat": {
    "name": "NAT",
    "short": "Network address translation: a router rewrites the addresses in packets passing through it, most often so that many privately addressed machines share one public address.",
    "def": "Private addresses cannot be routed on the internet, so something at the edge must swap them. With source NAT (masquerading), the gateway replaces the private source address of each outgoing packet with its own, remembers the mapping and reverses it on replies. Your home router does this, and so does a Docker host for its containers. The reverse direction, destination NAT, is how a published port works: traffic arriving at the host's port 8080 is rewritten to the container's address and port. Two consequences for evals: remote services see every container on a host as the same address, so rate limits and bans apply to all of them together; and nothing outside can open a connection to a container unless a port was published. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "network address translation, masquerade",
    "see": [
      "private-address-range",
      "default-gateway",
      "iptables",
      "bridge-network",
      "ingress"
    ]
  },
  "port": {
    "name": "Port",
    "short": "A number from 0 to 65535 that identifies which program on a machine a network connection is for, so that one IP address can host many services.",
    "def": "An IP address gets a packet to a machine; the port number gets it to the right program on that machine. A server claims a port and listens on it, and clients connect to address plus port: <code>10.0.0.5:443</code>. Conventions assign well-known numbers — 22 for SSH, 53 for DNS, 80 for HTTP, 443 for HTTPS, 5432 for PostgreSQL — and ports below 1024 have traditionally required root to claim. The client's end of a connection also uses a port, a temporary one chosen by the kernel. Only one program can listen on a given address and port at a time, so a leftover server from an earlier command produces <code>Address already in use</code> when the agent tries to start another. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "port number, TCP port",
    "see": [
      "socket",
      "listening-socket",
      "tcp",
      "udp",
      "bind-address"
    ]
  },
  "socket": {
    "name": "Socket",
    "short": "The kernel object a program uses as its endpoint for network communication; it is read and written through a file descriptor, much like a file.",
    "def": "A program that wants to talk over the network asks the kernel for a socket, then either connects it to a remote address and port or binds it to a local one and listens. From then on the program reads and writes the socket through a file descriptor, as it would a file — the everything-is-a-file idea applied to networking. An established TCP connection is identified by both ends together (local address and port, remote address and port), which is how one server port carries thousands of connections at once. <code>ss</code> lists a machine's sockets. There are also Unix domain sockets, which appear as paths on the filesystem and connect processes on one machine; <code>/var/run/docker.sock</code> is the one that matters for sandbox security. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a> and <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "network socket, Unix socket",
    "see": [
      "port",
      "listening-socket",
      "file-descriptor",
      "tcp",
      "docker-socket"
    ]
  },
  "tcp": {
    "name": "TCP",
    "short": "Transmission Control Protocol: the connection-based transport that delivers a reliable, ordered stream of bytes between two programs; HTTP, SSH and most services use it.",
    "def": "IP alone delivers individual packets on a best-effort basis: they may be lost, duplicated or reordered. TCP builds a dependable channel on top. The two sides first exchange a handshake to set up a connection, then number, acknowledge and retransmit data so the application sees a clean byte stream. The handshake is a useful diagnostic because it fails in two distinct ways. <code>Connection refused</code> comes back at once and means the machine answered but nothing is listening on that port. A timeout means no answer came at all — the address is wrong or, most often, a firewall is silently dropping the packets. Telling the two apart in a transcript separates a service that never started from a blocked network. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "Transmission Control Protocol",
    "see": [
      "udp",
      "port",
      "socket",
      "listening-socket",
      "firewall"
    ]
  },
  "udp": {
    "name": "UDP",
    "short": "User Datagram Protocol: a minimal transport that sends individual messages with no connection, no delivery guarantee and no ordering; DNS is its best-known user.",
    "def": "UDP adds port numbers to IP and very little else. A program sends a datagram and hopes; there is no handshake, acknowledgement or retransmission unless the application supplies its own. That suits short request-and-reply exchanges such as DNS lookups and time synchronisation, and traffic where a late packet is worthless. It has its own port space, so TCP port 53 and UDP port 53 are separate things, and <code>ss -u</code> lists UDP sockets separately from TCP ones. With no handshake, failure has no clear signal: a blocked UDP request simply never gets a reply. Firewall rules name a protocol, so a ruleset reviewed only for TCP may still leave UDP — and with it DNS — open as a path out of a sandbox. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "User Datagram Protocol",
    "see": [
      "tcp",
      "port",
      "dns",
      "socket",
      "egress"
    ]
  },
  "listening-socket": {
    "name": "Listening Socket",
    "short": "A socket that a server has bound to an address and port and marked as ready to accept incoming connections; it is what it means for a port to be open.",
    "def": "A server becomes reachable by creating a socket, binding it to an address and port, and calling <code>listen</code>. From that moment the kernel accepts connections on the program's behalf; with no listening socket on a port, connection attempts are refused. <code>ss -tlnp</code> shows them all: TCP (<code>t</code>), listening (<code>l</code>), numeric (<code>n</code>), with the owning process (<code>p</code>, which needs root to see other users' processes). This is a core audit command because it enumerates every way into the box from the network and names the program behind each. Run inside a task container, it also tells you whether the service the task depends on actually started before you blame the agent for failing to reach it. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a> and <a href='pages/28-ten-minute-audit.html'>The Ten-Minute Audit</a>.",
    "also": "open port, LISTEN, ss -tlnp",
    "see": [
      "socket",
      "port",
      "bind-address",
      "tcp",
      "attack-surface"
    ]
  },
  "bind-address": {
    "name": "Bind Address",
    "short": "The local address a server listens on: 127.0.0.1 accepts connections only from the same machine, while 0.0.0.0 accepts them on every interface.",
    "def": "A listening socket is tied to a port and also to a local address, and the address decides who can connect. Bound to <code>127.0.0.1</code>, the service is reachable only through loopback, from the same machine. Bound to <code>0.0.0.0</code>, meaning all IPv4 addresses, it is reachable through every interface. Many development servers default to 127.0.0.1 for safety, which is the classic container puzzle: the server runs, the port is published, and connections from the host still fail, because inside the container it listens only on the container's own loopback. The fix is to bind 0.0.0.0 inside the container and restrict exposure at the publishing step. The local-address column of <code>ss -tln</code> shows the bind address. See <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "0.0.0.0, listen address",
    "see": [
      "listening-socket",
      "loopback",
      "localhost",
      "port",
      "ingress"
    ]
  },
  "dns": {
    "name": "DNS",
    "short": "The Domain Name System: the distributed directory that translates hostnames such as pypi.org into the IP addresses needed to connect to them.",
    "def": "Networks route on addresses, people and configuration files use names, and DNS bridges the two. A program hands a name to the system's resolver, which queries a DNS server — conventionally on port 53, over UDP first — and receives one or more addresses. Since nearly every connection begins with a lookup, broken DNS looks like a broken network even when routing is fine: the errors are <code>Could not resolve host</code> or <code>Temporary failure in name resolution</code>, not refused or timed out. Test the layers separately: <code>dig example.com</code> exercises DNS alone, while <code>curl</code> to a raw IP address skips it. DNS is also an outbound channel, so a sandbox meant to have no egress should be checked for whether lookups of external names still succeed. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "Domain Name System, name resolution",
    "see": [
      "resolver",
      "hosts-file",
      "udp",
      "egress",
      "ip-address"
    ]
  },
  "resolver": {
    "name": "Resolver",
    "short": "The part of the system that turns a hostname into an address on behalf of programs, configured chiefly by /etc/resolv.conf, which names the DNS servers to ask.",
    "def": "Programs do not speak DNS themselves; they call a library function, and the resolver does the rest. On Linux it consults sources in the order set by the <code>hosts</code> line of <code>/etc/nsswitch.conf</code> — normally <code>files dns</code>, meaning <code>/etc/hosts</code> first, then the servers listed as <code>nameserver</code> lines in <code>/etc/resolv.conf</code>. On an Ubuntu machine that server is usually a local caching stub at <code>127.0.0.53</code>; in a container Docker writes the file, pointing at the host's DNS or, on user-defined networks, at its built-in server at <code>127.0.0.11</code>, which also resolves container names. Note that <code>dig</code> queries DNS directly and ignores <code>/etc/hosts</code>, whereas <code>getent hosts name</code> answers the way ordinary programs do. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "/etc/resolv.conf, stub resolver",
    "see": [
      "dns",
      "hosts-file",
      "localhost",
      "bridge-network"
    ]
  },
  "hosts-file": {
    "name": "/etc/hosts",
    "short": "A plain-text file mapping hostnames to IP addresses that the system normally consults before DNS; it is where localhost is defined.",
    "def": "Each line of <code>/etc/hosts</code> is an address followed by one or more names, and because the resolver normally reads this file first, an entry here overrides DNS for that name on this machine. It is how <code>localhost</code> resolves with no network, and how you give a test service a name without running a DNS server. In a container Docker generates the file, adding the container's own hostname and anything passed with <code>--add-host</code>. Two cautions. It is no security control: pointing a domain at <code>127.0.0.1</code> does not stop an agent running as root from editing the file or connecting by IP address. And tools that query DNS directly, such as <code>dig</code>, never consult it. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "hosts file",
    "see": [
      "resolver",
      "dns",
      "localhost",
      "allowlist"
    ]
  },
  "http": {
    "name": "HTTP",
    "short": "The request-and-response protocol of the web and of nearly every API: a client sends a method, a path and headers, and the server answers with a status code and a body.",
    "def": "HTTP is text-structured and simple at heart. The client opens a TCP connection (port 80, or 443 when wrapped in TLS), sends a request line such as <code>GET /v1/models</code>, headers and perhaps a body; the server replies with a status code, headers and a body. The first digit of the status tells you whose problem it is: 2xx success, 3xx redirect, 4xx the request was wrong (401 unauthenticated, 404 not found, 429 rate-limited), 5xx the server failed. <code>curl -v</code> prints the whole exchange and is the standard way to see what actually went over the wire. Model APIs, package downloads, and often the harness's own channel to the sandbox are all HTTP, so reading a status line is how you separate bad credentials from a blocked network. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "HTTPS, status code, curl",
    "see": [
      "tls",
      "tcp",
      "proxy",
      "port",
      "dns"
    ]
  },
  "tls": {
    "name": "TLS",
    "short": "Transport Layer Security: the protocol that encrypts a connection and verifies the server's identity; HTTPS is simply HTTP carried inside TLS.",
    "def": "A plain TCP connection can be read and altered by anything on the path. TLS wraps it: during a handshake the server presents a certificate, the client checks it against authorities it already trusts and against the name it meant to reach, and the two agree on encryption keys. After that the application protocol runs unchanged inside the tunnel, so HTTPS is HTTP over TLS, conventionally on port 443. In sandboxes, TLS problems are rarely about cryptography. They come from the environment: a minimal image with no CA certificates installed, a system clock that is wrong, or an inspecting proxy whose certificate the container does not trust. <code>curl -v</code> shows the handshake and the precise complaint. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "SSL, HTTPS",
    "see": [
      "certificate",
      "http",
      "proxy",
      "tcp"
    ]
  },
  "certificate": {
    "name": "Certificate",
    "short": "A signed file binding a public key to a hostname, presented by a TLS server to prove its identity; clients trust it if it chains to a certificate authority they know.",
    "def": "When you connect to <code>https://pypi.org</code>, the server sends a certificate stating that this key belongs to pypi.org, signed by a certificate authority (CA). Your side verifies the signature chain up to one of the root CAs it already trusts, and checks the hostname and validity dates. On Debian and Ubuntu the trusted roots come from the <code>ca-certificates</code> package under <code>/etc/ssl/certs</code> — and the <code>ubuntu:24.04</code> image does not include it, so HTTPS requests fail verification there until it is installed. Agents commonly react by switching verification off (<code>curl -k</code>, <code>verify=False</code>), which hides the real fault. An organisation's TLS-inspecting proxy causes the same error until its CA is added to the trust store. See <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "TLS certificate, CA, ca-certificates",
    "see": [
      "tls",
      "http",
      "proxy",
      "base-image"
    ]
  },
  "proxy": {
    "name": "Proxy",
    "short": "An intermediary server that makes network requests on behalf of clients, giving one controlled point at which traffic can be filtered, logged or cached.",
    "def": "With a forward proxy, the client sends its request to the proxy, which connects to the real destination and relays the answer. Most command-line tools find the proxy through environment variables — <code>HTTP_PROXY</code>, <code>HTTPS_PROXY</code> and <code>NO_PROXY</code> for exceptions — though not every program honours them. In sandbox design a proxy is the practical way to enforce a domain allowlist. A packet firewall sees only IP addresses, which change constantly for sites behind content delivery networks, whereas a proxy sees the requested hostname. The pattern is to block all direct egress by firewall, allow only the proxy, and let the proxy decide by domain and keep a log. That log doubles as the record of everything the agent tried to reach. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a> and <a href='pages/18-dns-http-tls.html'>DNS, HTTP, and TLS</a>.",
    "also": "forward proxy, HTTP_PROXY",
    "see": [
      "egress",
      "allowlist",
      "firewall",
      "http",
      "environment-variable"
    ]
  },
  "egress": {
    "name": "Egress",
    "short": "Network traffic leaving a machine or sandbox for somewhere else; egress control decides what, if anything, an agent inside can reach.",
    "def": "Egress is the outbound direction: connections that start inside the sandbox and go out. For evaluation it is the direction that matters most. An agent with open internet access can look up a benchmark task's published solution, download the fixed version of the repository, call another model for help, or send data out — each of which makes the score measure something other than the agent's own ability. Options run from none (<code>docker run --network none</code>), through a default-deny firewall with an allowlist, to fully open. Whichever you choose, verify it from inside the box, and test more than one route: a raw IP address, a DNS lookup, an HTTPS request, and the cloud metadata address. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "outbound traffic, egress control",
    "see": [
      "ingress",
      "firewall",
      "default-deny",
      "allowlist",
      "solution-leakage"
    ]
  },
  "ingress": {
    "name": "Ingress",
    "short": "Network traffic arriving at a machine or sandbox from outside: connections that something else initiates towards a service listening inside.",
    "def": "Ingress is the inbound direction — who can connect to what is listening here. A container on Docker's default network is unreachable from outside the host until you publish a port with <code>-p</code>, and harnesses rarely need any, since they drive the sandbox through the container runtime rather than over its network. The thing to watch is how publishing binds. <code>-p 8080:80</code> listens on every interface of the host, not just loopback, so a task's web application may be exposed to the whole local network; writing <code>-p 127.0.0.1:8080:80</code> keeps it local. On a shared or cloud host, every open listening port is attack surface and should be deliberate. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a> and <a href='pages/17-ports-and-sockets.html'>Ports, Sockets, TCP and UDP</a>.",
    "also": "inbound traffic, published port",
    "see": [
      "egress",
      "listening-socket",
      "bind-address",
      "firewall",
      "attack-surface"
    ]
  },
  "firewall": {
    "name": "Firewall",
    "short": "Rules, enforced by the kernel on Linux, that decide which network packets are allowed through, based on direction, addresses, ports and protocol.",
    "def": "A Linux firewall is a list of rules the kernel's netfilter layer checks against each packet: match on direction, interface, source and destination address, protocol, port and connection state, then accept, drop or reject. Dropping discards silently, so the sender waits for a timeout; rejecting sends back an error, so the sender fails immediately — a difference you can read in a transcript. The rules are managed with <code>nft</code> or the older <code>iptables</code>. For a sandbox the firewall must sit where the agent cannot alter it: on the host or in a separate network layer, not inside a container in which the agent is root with network-administration capabilities. And it must be tested by attempting connections, because a ruleset that reads correctly can still be wrong. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "packet filter, netfilter",
    "see": [
      "nftables",
      "iptables",
      "default-deny",
      "egress",
      "allowlist"
    ]
  },
  "default-deny": {
    "name": "Default Deny",
    "short": "A firewall stance in which everything is blocked unless a rule explicitly allows it, as opposed to allowing everything except what is listed.",
    "def": "Every ruleset has to say what happens to a packet that matches no rule. Default allow means you list the bad things and everything else passes, including all the bad things you did not think of. Default deny reverses it: the base policy is drop, and you add narrow exceptions for what the task needs. It is least privilege applied to the network, and it fails safe — an omission breaks a task visibly rather than leaving a hole silently. For sandboxes you cannot enumerate every site that might host a benchmark's answers, so a blocklist is unworkable and default deny is the only defensible starting point. Remember that the policy must cover IPv6 and UDP as well as IPv4 TCP. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "deny by default, default drop",
    "see": [
      "allowlist",
      "firewall",
      "egress",
      "least-privilege",
      "nftables"
    ]
  },
  "allowlist": {
    "name": "Allowlist",
    "short": "An explicit list of the destinations, or other items, that are permitted, with everything not on the list refused.",
    "def": "An allowlist is the set of exceptions that makes a default-deny policy usable: this package mirror, that model API, nothing else. The difficulty is that people think in domain names while packet firewalls match IP addresses. A large site's addresses change frequently and are shared with unrelated sites on the same delivery network, so an address-based allowlist is at once too fragile and too broad. Hence the usual design of an HTTP proxy that allows by hostname, with the firewall permitting traffic only to the proxy. Audit every entry for what else it enables: allowing a code-hosting site for one dependency also allows reaching any repository there, including ones containing benchmark solutions. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "whitelist",
    "see": [
      "default-deny",
      "proxy",
      "egress",
      "firewall",
      "solution-leakage"
    ]
  },
  "nftables": {
    "name": "nftables",
    "short": "The current Linux packet-filtering framework, configured with the nft command; it is the successor to iptables and handles IPv4 and IPv6 in one ruleset.",
    "def": "nftables is the modern interface to the kernel's packet filter. Rules live in tables, which hold chains attached to hooks — input, output, forward — and each chain has a default policy plus an ordered list of rules. <code>nft list ruleset</code> prints everything in one readable block, which is the audit command to remember. A table of family <code>inet</code> covers IPv4 and IPv6 together, closing the gap that separate rulesets used to leave. On current Debian and Ubuntu even the <code>iptables</code> command is normally a compatibility front end feeding the same kernel machinery. Both need root and a network namespace of your own, which is why the course uses a VM, not a container, for firewall labs. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "nft",
    "see": [
      "iptables",
      "firewall",
      "default-deny",
      "egress",
      "ipv6"
    ]
  },
  "iptables": {
    "name": "iptables",
    "short": "The long-standing Linux command for configuring packet-filtering and NAT rules; superseded by nftables but still everywhere, including in Docker's own networking.",
    "def": "iptables organises rules into tables (<code>filter</code> for allow and deny, <code>nat</code> for address rewriting), each containing chains such as INPUT, OUTPUT and FORWARD that packets pass through in order. <code>iptables -S</code> or <code>iptables -L -n -v</code> lists the rules. You need to read it because so much existing material uses it: tutorials, sandbox setup scripts, and Docker, which programs iptables rules on the host to implement container NAT and published ports. Two cautions. IPv6 has a separate command, <code>ip6tables</code>, so an egress block written only in iptables does not cover IPv6. And Docker inserts its own rules, which can let traffic to published ports through in spite of a host firewall you believed was closed. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "ip6tables, netfilter",
    "see": [
      "nftables",
      "firewall",
      "nat",
      "egress",
      "docker"
    ]
  },
  "bridge-network": {
    "name": "Bridge Network",
    "short": "Docker's default kind of container network: a virtual switch inside the host to which containers attach, each with a private address, reaching the outside through NAT.",
    "def": "A Linux bridge is a software Ethernet switch. Docker creates one, <code>docker0</code>, typically with the subnet <code>172.17.0.0/16</code>, plugs each new container into it and gives the container the bridge's address as its default gateway; outbound traffic is NATed to the host's address. Containers on the same bridge can reach one another directly. Networks you define yourself, including the ones Compose creates, behave the same way but add DNS, so containers find each other by name. For evals the consequences are two. Unless you choose otherwise every container gets outbound internet access, and samples running side by side on one bridge can reach each other. Use <code>--network none</code>, or a separate internal network per sample, when that matters. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "docker0, bridge",
    "see": [
      "veth",
      "nat",
      "network-namespace",
      "default-gateway",
      "subnet"
    ]
  },
  "veth": {
    "name": "veth Pair",
    "short": "A pair of linked virtual network interfaces acting like a cable: whatever enters one end comes out of the other, used to connect a container to the host's network.",
    "def": "A new network namespace contains nothing but its own loopback interface, so it is cut off from everything. To connect it, the kernel offers virtual Ethernet devices that are created in pairs. The container runtime moves one end into the container's namespace, where it appears as <code>eth0</code>, and leaves the other end on the host attached to a bridge, where it shows up in <code>ip link</code> under a name beginning with <code>veth</code>. That is the whole trick behind container networking: a virtual cable from a private namespace to a virtual switch. Knowing it lets you find, on the host, the exact interface carrying one container's traffic, which is where you would capture its packets or apply a rule to that container alone. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a>.",
    "also": "virtual Ethernet",
    "see": [
      "network-namespace",
      "bridge-network",
      "network-interface",
      "packet-capture"
    ]
  },
  "packet-capture": {
    "name": "Packet Capture",
    "short": "Recording the actual packets crossing a network interface, typically with tcpdump, to see what was really sent and received.",
    "def": "When claims about the network conflict — the application says it sent the request, the server says nothing arrived — a capture settles it. <code>tcpdump -n -i eth0 port 53</code> prints each matching packet as it passes; <code>-n</code> skips name lookups, <code>-i any</code> watches every interface and <code>-w file.pcap</code> saves the capture for Wireshark. Capturing needs root or the equivalent network capabilities, and the tool is rarely present in task images, so capture from the host side of the container's interface instead. For sandbox work it is the strongest available evidence about egress. A capture taken on the host during a run shows every destination the container attempted to reach, whatever the agent's transcript says or leaves out. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "tcpdump, pcap",
    "see": [
      "network-interface",
      "veth",
      "egress",
      "firewall",
      "environment-integrity"
    ]
  },
  "icmp": {
    "name": "ICMP",
    "short": "Internet Control Message Protocol: the network's error-and-diagnostics channel, best known as what ping uses to test whether a host answers.",
    "def": "ICMP carries messages about the network itself instead of application data: destination unreachable, time exceeded, and the echo request and reply behind <code>ping</code>. It has no ports, so rules written in terms of ports do not describe it, and firewalls treat it as its own protocol. That makes ping a weaker test than it appears. A failed ping may only mean ICMP is filtered while TCP port 443 works; a successful ping proves the host is up and says nothing about whether the port you need is open. To test reachability of a service, attempt a real connection with <code>curl</code> or <code>nc -zv host port</code>. Minimal images usually lack <code>ping</code> anyway; on Ubuntu it is in the <code>iputils-ping</code> package. See <a href='pages/16-addresses-and-routes.html'>Addresses, Interfaces, and Routes</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "ping",
    "see": [
      "tcp",
      "udp",
      "firewall",
      "ip-address",
      "egress"
    ]
  },
  "metadata-service": {
    "name": "Metadata Service",
    "short": "An HTTP endpoint at the fixed address 169.254.169.254 that cloud providers expose to each VM, serving details about the instance and often temporary credentials.",
    "def": "Cloud virtual machines learn about themselves — instance name, region, startup scripts, and the temporary credentials for whatever role is attached — by requesting them from a link-local address, <code>169.254.169.254</code>, which the platform answers from within the host. No password is needed, because being on the VM is treated as the proof of identity. A container on that VM is on the VM too. Unless the address is blocked, an agent in a sandbox hosted on a cloud instance can query it and may obtain credentials carrying the instance's permissions — a route to secrets that appears nowhere in the environment or the filesystem. Include the address in every egress reachability test, and give instances that run sandboxes the narrowest role you can. See <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a> and <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "instance metadata, IMDS, 169.254.169.254",
    "see": [
      "secret",
      "egress",
      "default-deny",
      "trust-boundary",
      "least-privilege"
    ]
  },
  "container": {
    "name": "Container",
    "short": "An ordinary Linux process (or group of them) that the kernel shows a restricted view of the system: its own filesystem, process list, network, and resource limits, while sharing the host's kernel.",
    "def": "A container is not a small virtual machine; it is a normal Linux process that was started with extra kernel bookkeeping. <a href='pages/20-namespaces.html'>Namespaces</a> decide what the process can see (its own root filesystem, PID numbers, network interfaces, hostname), cgroups decide how much it can use, and capabilities and seccomp decide what it may ask the kernel to do. Containers exist because this is far cheaper than booting a whole machine: starting one takes about as long as starting a process. The price is that every container on a host shares one kernel, so a kernel bug is a shared weakness. Most agentic benchmarks run each task in a container, which means the properties of your sandbox are exactly the properties of these mechanisms, as configured. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "see": [
      "namespace",
      "cgroup",
      "image",
      "isolation",
      "virtual-machine"
    ]
  },
  "image": {
    "name": "Image",
    "short": "A read-only, packaged filesystem plus metadata (default command, environment variables, user) from which containers are started; the template, where a container is the running instance.",
    "def": "An image is a packaged root filesystem, stored as a stack of read-only <a href='pages/22-docker-for-evals.html'>layers</a>, plus a small config recording the default command, environment variables, working directory, and user. Starting a container means giving a process that filesystem with a thin writable layer on top; the image itself never changes. Images exist so that an environment can be built once and started identically many times, on any machine. For an evals engineer the image is the specification of the task environment: which tools are installed, which versions, which files the agent can find. Anything baked into the image, including an answer key someone copied in by accident, is visible to every run. Refer to images by digest, not by tag, if you need runs to be comparable.",
    "also": "container image, Docker image",
    "see": [
      "layer",
      "dockerfile",
      "image-digest",
      "tag",
      "task-image"
    ]
  },
  "layer": {
    "name": "Layer",
    "short": "One read-only filesystem diff inside an image, usually produced by a single Dockerfile instruction; layers are stacked to form the container's filesystem.",
    "def": "A layer is a recorded set of filesystem changes: files added, modified, or marked deleted by one build step. An image is an ordered stack of layers, and at run time a union filesystem (overlayfs on a typical Docker install) presents the stack as one directory tree with a writable layer on top. Layers exist so that builds can be cached and images that share a base can share storage and downloads. The consequence that catches people: deleting a file in a later layer only hides it. The bytes still sit in the earlier layer, and anyone with the image can extract them. A Dockerfile that copies in reference solutions and then runs <code>rm</code> has not removed them from the image. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/14-mounts-and-filesystems.html'>Mounts and Filesystems</a>.",
    "see": [
      "image",
      "overlayfs",
      "dockerfile",
      "solution-leakage"
    ]
  },
  "dockerfile": {
    "name": "Dockerfile",
    "short": "A text file of build instructions (FROM, RUN, COPY, USER, ENTRYPOINT…) that Docker executes in order to produce an image.",
    "def": "A Dockerfile is the recipe for an image: start <code>FROM</code> a base image, <code>RUN</code> commands to install software, <code>COPY</code> files in, set the <code>USER</code>, <code>WORKDIR</code>, and the default command. Each instruction that changes the filesystem produces a layer. It exists so that an environment is described in a reviewable file instead of being assembled by hand. Read one the way you would read a lab protocol. <code>FROM ubuntu:latest</code> and an unpinned <code>apt-get install</code> mean the image you build next month differs from the one you built today, so scores drift for reasons that have nothing to do with the model. No <code>USER</code> line means the agent runs as root. A <code>COPY . .</code> may drag in tests or solutions you never meant to ship. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a>.",
    "see": [
      "image",
      "layer",
      "base-image",
      "version-pinning",
      "entrypoint"
    ]
  },
  "docker": {
    "name": "Docker",
    "short": "The most widely used toolset for building images and running containers: a command-line client that talks to a background daemon, which sets up namespaces, cgroups, and networking for you.",
    "def": "Docker is a packaging of kernel features into a usable tool. The <code>docker</code> command is a client; it sends requests to the Docker daemon, which pulls images, creates the namespaces and cgroups, wires up a network, and starts your process. Nothing Docker does is magic: every <code>docker run</code> flag maps onto a mechanism from <a href='pages/20-namespaces.html'>pages 20</a> and <a href='pages/21-cgroups-capabilities-seccomp.html'>21</a> (<code>--memory</code> is a cgroup limit, <code>--network none</code> is an empty network namespace, <code>--cap-drop</code> edits the capability set). On a Mac, Docker Desktop runs a hidden Linux virtual machine, because containers need a Linux kernel. Docker is the default sandbox of agentic evals, so reading a harness's Docker configuration is how you learn what the agent was actually allowed to do. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "see": [
      "container",
      "docker-daemon",
      "image",
      "docker-compose",
      "container-runtime"
    ]
  },
  "docker-daemon": {
    "name": "Docker Daemon",
    "short": "The long-running background service (dockerd) that actually builds images and creates containers; by default it runs as root and takes orders from the docker client over a socket.",
    "def": "The Docker daemon, <code>dockerd</code>, is the server half of Docker. The <code>docker</code> command you type only sends API requests; the daemon does the privileged work of creating namespaces, mounting filesystems, and configuring networks, which is why in the default setup it runs as root. That design has a direct security consequence: whoever can send requests to the daemon can ask it to start a container with the host's filesystem mounted, so control of the daemon is equivalent to root on the host. Docker's own documentation says only trusted users should be allowed to control it. In an eval, the harness talks to the daemon and the agent must not be able to. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "dockerd",
    "see": [
      "docker",
      "docker-socket",
      "daemon",
      "rootless",
      "trust-boundary"
    ]
  },
  "docker-socket": {
    "name": "Docker Socket",
    "short": "The Unix socket file, normally /var/run/docker.sock, through which clients send commands to the Docker daemon; access to it is effectively root access to the host.",
    "def": "The Docker socket is a Unix domain socket at <code>/var/run/docker.sock</code>: a file that acts as the daemon's front door. It is protected by ordinary file permissions (owned by root, with group <code>docker</code>), and that is all that protects it. Any process that can write to the socket can tell the daemon to start a new container with any mount and any privilege, so it can read and modify the host. People bind-mount the socket into a container to let it launch sibling containers; doing that to a container an agent controls removes the sandbox entirely. The audit check is simple: look for <code>docker.sock</code> in the container's mounts (<code>findmnt</code>, <code>docker inspect</code>) and make sure it is not there. See <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "docker.sock",
    "see": [
      "docker-daemon",
      "socket",
      "bind-mount",
      "container-escape",
      "privilege-escalation"
    ]
  },
  "docker-compose": {
    "name": "Docker Compose",
    "short": "A tool that starts a group of related containers, networks, and volumes from one declarative YAML file (compose.yaml) instead of a series of long docker run commands.",
    "def": "Docker Compose describes a multi-container setup in one file: each service's image or build context, its mounts, environment variables, resource limits, and the networks that connect services. <code>docker compose up</code> creates it all; <code>docker compose down</code> removes it. It exists because real environments are rarely one container: a task might need the agent's box, a database, and a mock web service, reachable from each other and from nothing else. Harnesses lean on it for the same reason; Inspect's Docker sandbox, for example, is configured with a <code>compose.yaml</code>. When you audit an eval, the compose file is where the facts live: which network the agent's container is on, what is mounted and whether read-only, and what memory and CPU limits apply. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "compose, compose.yaml",
    "see": [
      "docker",
      "container",
      "bridge-network",
      "volume",
      "inspect"
    ]
  },
  "registry": {
    "name": "Registry",
    "short": "A server that stores container images and serves them by name, such as Docker Hub; docker pull downloads from one and docker push uploads to one.",
    "def": "A registry is a storage service for images. An image name like <code>ubuntu:24.04</code> is shorthand for a repository on a default registry (Docker Hub); a name with a hostname in front points at a different one. Registries exist so an image built once can be fetched by any machine that needs it, layer by layer, skipping layers it already has. Two things matter for evals. First, a registry is a network dependency: a harness that pulls images at run time fails, or is rate-limited, when the registry is unreachable, and that is an infrastructure failure, not a model failure. Second, a tag on a registry can be re-pointed to new content at any time, so pulling by tag does not guarantee the same environment twice; pulling by digest does. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "also": "container registry, Docker Hub",
    "see": [
      "image",
      "tag",
      "image-digest",
      "repository",
      "infrastructure-failure"
    ]
  },
  "image-digest": {
    "name": "Image Digest",
    "short": "A SHA-256 hash of an image's content, written image@sha256:…, that identifies exactly one immutable image, unlike a tag, which can be moved.",
    "def": "A digest is a cryptographic hash computed from an image's content. Because any change to the content changes the hash, <code>ubuntu@sha256:…</code> names one specific image forever, and Docker verifies what it downloaded against it. Digests exist because tags are only labels: <code>python:3.12</code> points at whatever the publisher most recently pushed under that name. For a benchmark this is the difference between a fixed instrument and a drifting one. If the base image silently gains a newer library, a task can become easier, harder, or broken, and the score changes with no change to the model. Pin <code>FROM</code> lines and task images by digest, and record the digest in the run log so a result can be reproduced later. See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "also": "sha256 digest",
    "see": [
      "tag",
      "image",
      "version-pinning",
      "reproducible-build",
      "registry"
    ]
  },
  "tag": {
    "name": "Tag",
    "short": "The human-readable label after the colon in an image name (ubuntu:24.04, python:latest); a movable pointer to an image, not a fixed identity.",
    "def": "A tag is a name a publisher attaches to an image in a repository, such as <code>24.04</code> or <code>latest</code>. If you give no tag, Docker assumes <code>latest</code>, which is only a conventional name and carries no guarantee of being the newest anything. Tags exist for convenience: people want to say <q>the current 24.04 image</q> without quoting a hash. The catch is that a tag is mutable. Publishers routinely rebuild and re-push the same tag to pick up security updates, so the same <code>docker pull</code> returns different content on different days. That is fine for a laptop and a problem for a benchmark, where two runs a month apart are supposed to be measuring the same thing. Use tags to find an image and digests to pin it. See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "also": "image tag",
    "see": [
      "image-digest",
      "image",
      "registry",
      "version-pinning"
    ]
  },
  "entrypoint": {
    "name": "Entrypoint",
    "short": "The command an image is configured to run when a container starts; that process becomes PID 1 inside the container and the container lives exactly as long as it does.",
    "def": "An image's config names the program to start, set in a Dockerfile with <code>ENTRYPOINT</code> and <code>CMD</code> (roughly: the fixed command, and its default arguments, which <code>docker run</code> arguments replace). Whatever starts becomes PID 1 in the container's PID namespace, and when it exits the container stops. Two details follow from mechanisms elsewhere in the course. Written in shell form (<code>ENTRYPOINT my-server --flag</code>), the command runs under <code>/bin/sh -c</code>, so the shell is PID 1 and your program may never receive the <code>SIGTERM</code> that <code>docker stop</code> sends. And PID 1 gets special signal treatment from the kernel, which is why containers that ignore a polite stop are eventually killed. Harnesses often override the entrypoint with something like <code>sleep infinity</code> and drive the box with <code>docker exec</code>. See <a href='pages/22-docker-for-evals.html'>page 22</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "ENTRYPOINT, CMD",
    "see": [
      "pid-1",
      "dockerfile",
      "sigterm",
      "container",
      "pid-namespace"
    ]
  },
  "namespace": {
    "name": "Namespace",
    "short": "A kernel feature that gives a group of processes their own private view of one global resource, such as the process list, the mount table, the network stack, or the hostname.",
    "def": "Normally every process on a machine sees the same process list, the same mounts, the same network interfaces. A namespace wraps one such global resource so that processes inside it see their own isolated instance, and changes are invisible outside. Linux has several kinds (mount, PID, network, user, UTS, IPC, cgroup, time), and a process belongs to one of each. A <q>container</q> is just a process placed in a fresh set of them. Namespaces control <em>visibility</em>, not consumption or permitted operations; those are the jobs of cgroups, capabilities, and seccomp. You can list them with <code>lsns</code> and look at any process's membership under <code>/proc/&lt;pid&gt;/ns</code>. For auditing a sandbox, the useful question is always which namespaces are <em>not</em> separate: a container started with <code>--network host</code> or <code>--pid host</code> shares that view with the host. See <a href='pages/20-namespaces.html'>Namespaces: What a Container Really Is</a>.",
    "see": [
      "pid-namespace",
      "mount-namespace",
      "network-namespace",
      "user-namespace",
      "container"
    ]
  },
  "pid-namespace": {
    "name": "PID Namespace",
    "short": "A namespace with its own process ID numbering: the first process inside is PID 1, and processes inside cannot see or signal processes outside.",
    "def": "A PID namespace gives a set of processes a private numbering starting from 1. Run <code>ps</code> in a container and you see a handful of processes, not the host's hundreds; the same processes are visible from the host under different, larger PIDs. The first process in the namespace takes on the role of init: orphaned children are re-parented to it, the kernel delivers to it only signals it has installed a handler for (when sent from inside), and when it exits the kernel kills everything else in the namespace with <code>SIGKILL</code>. That explains two things you will see in transcripts: zombies piling up under an entrypoint that never reaps them, and background jobs an agent started vanishing the instant the main process ends. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "see": [
      "namespace",
      "pid-1",
      "pid",
      "zombie-process",
      "entrypoint"
    ]
  },
  "mount-namespace": {
    "name": "Mount Namespace",
    "short": "A namespace with its own mount table, so a group of processes can have a completely different filesystem tree from the host, including a different root directory.",
    "def": "The mount table is the kernel's list of which filesystem is attached at which directory. A mount namespace gives a process group a private copy of that list: mounts made inside are not seen outside. Combined with switching the root directory to an image's unpacked filesystem (<code>pivot_root</code>), this is how a container gets its own <code>/</code> with its own <code>/etc</code> and <code>/usr</code> while the host's files are simply not reachable by any path. For eval work, the mount table is where you verify claims about the environment: <code>findmnt</code> inside the sandbox shows every bind mount from the host, and whether each is <code>ro</code> or <code>rw</code>. A test directory bind-mounted read-write is one the agent can edit. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/14-mounts-and-filesystems.html'>Mounts and Filesystems</a>.",
    "see": [
      "namespace",
      "mount",
      "bind-mount",
      "read-only-mount",
      "chroot"
    ]
  },
  "network-namespace": {
    "name": "Network Namespace",
    "short": "A namespace with its own network stack: its own interfaces, IP addresses, routing table, firewall rules, and port numbers, separate from the host's.",
    "def": "A network namespace is a private copy of the kernel's networking state. A brand-new one contains only a loopback interface, and that one is down: no route to anywhere. Connectivity has to be added deliberately, typically with a veth pair, a virtual cable with one end inside the namespace and the other on a bridge on the host. It exists so that each container can bind port 80, have its own <code>localhost</code>, and be firewalled independently. This is the mechanism behind <code>docker run --network none</code>: the agent gets the empty namespace and nothing is plugged in, the strongest and simplest form of egress control. It is also why <code>localhost</code> inside a container is not the host's <code>localhost</code>, a standard cause of <q>connection refused</q> in transcripts. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/19-firewalls-and-egress.html'>Firewalls and Egress Control</a>.",
    "also": "netns",
    "see": [
      "namespace",
      "veth",
      "bridge-network",
      "egress",
      "loopback"
    ]
  },
  "user-namespace": {
    "name": "User Namespace",
    "short": "A namespace with its own mapping of user and group IDs, so a process can be UID 0 (root) inside while being an ordinary unprivileged user as far as the host is concerned.",
    "def": "A user namespace translates IDs: a mapping says that UID 0 inside corresponds to, say, UID 100000 outside. Inside, the process looks like root and holds capabilities, but those capabilities apply only to resources owned by that namespace; to the rest of the system it is user 100000 with no special rights. It exists to make <q>root in the container</q> stop meaning <q>root on the host</q>, and it is the foundation of rootless containers. The point to remember when auditing: a standard Docker setup does <em>not</em> put containers in a separate user namespace unless configured to (<code>userns-remap</code> or rootless mode). There, UID 0 in the container is the host's UID 0, held back only by the reduced capability set, seccomp, and the other namespaces. Check <code>/proc/self/uid_map</code> to see which situation you are in. See <a href='pages/20-namespaces.html'>Namespaces</a> and <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "userns",
    "see": [
      "namespace",
      "uid",
      "root-user",
      "rootless",
      "capability"
    ]
  },
  "uts-namespace": {
    "name": "UTS Namespace",
    "short": "The namespace that isolates the hostname (and NIS domain name), letting each container have its own hostname without affecting the host.",
    "def": "The UTS namespace isolates two small pieces of system identity: the hostname and the NIS domain name. (UTS stands for <q>UNIX Time-sharing System</q>, from the name of the kernel structure that holds them.) It exists so a container can call itself <code>web-1</code> or have its hostname set by an orchestrator without renaming the machine it runs on. It is the simplest namespace, which makes it the ideal first experiment: <code>unshare --uts</code>, change the hostname, and confirm from another terminal that the host's is untouched. In eval work it explains the random hex string in shell prompts inside transcripts (Docker sets the hostname to the container ID by default), and a hostname that matches the host's is a quick hint that a container was started with host namespaces shared. See <a href='pages/20-namespaces.html'>Namespaces: What a Container Really Is</a>.",
    "see": [
      "namespace",
      "container",
      "pid-namespace",
      "network-namespace"
    ]
  },
  "cgroup": {
    "name": "Cgroup",
    "short": "A control group: a kernel mechanism that puts processes into a group and meters and limits the group's total memory, CPU time, number of processes, and I/O.",
    "def": "Namespaces limit what a process can see; cgroups limit what it can use. A cgroup is a directory under <code>/sys/fs/cgroup</code>; processes are assigned to it, and files in it set limits for the whole group: <code>memory.max</code>, <code>cpu.max</code>, <code>pids.max</code> in cgroup v2, the version Ubuntu 24.04 uses. Docker's <code>--memory</code>, <code>--cpus</code>, and <code>--pids-limit</code> flags just write these files. They exist because per-process limits are trivially dodged by starting more processes; a group limit is not. When a group hits its memory limit and nothing can be reclaimed, the OOM killer kills a process in it, which shows up as exit code 137 with no error message. A benchmark without limits lets one runaway task starve its neighbours; one with limits set too tight scores resource exhaustion as model failure. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a> and <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "control group, cgroup v2",
    "see": [
      "oom-killer",
      "rlimit",
      "namespace",
      "container",
      "infrastructure-failure"
    ]
  },
  "capability": {
    "name": "Capability",
    "short": "One named slice of root's power, such as CAP_NET_ADMIN or CAP_SYS_ADMIN, that can be granted or removed individually so a process gets only the privileges it needs.",
    "def": "Traditionally Linux had two privilege levels: root, which bypasses every permission check, and everyone else. Capabilities split root's power into separately switchable units: <code>CAP_NET_BIND_SERVICE</code> to bind low ports, <code>CAP_CHOWN</code> to change file ownership, <code>CAP_NET_ADMIN</code> to configure networking, <code>CAP_SYS_ADMIN</code> for a large grab-bag including mounting filesystems. They exist so that <q>needs one privileged operation</q> no longer means <q>gets all of them</q>. Docker starts containers, even those running as root, with a reduced set, which is why root in a container cannot load kernel modules or change firewall rules by default. <code>--cap-drop ALL</code> removes the rest; <code>--cap-add</code> and <code>--privileged</code> hand power back. To audit, read <code>CapEff</code> in <code>/proc/self/status</code> and decode it with <code>capsh --decode</code>. An agent container holding <code>CAP_SYS_ADMIN</code> deserves an explanation. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a>.",
    "also": "Linux capabilities, CAP_*",
    "see": [
      "root-user",
      "least-privilege",
      "privileged-container",
      "seccomp",
      "no-new-privileges"
    ]
  },
  "seccomp": {
    "name": "Seccomp",
    "short": "A kernel facility that filters the system calls a process is allowed to make, so that calls it has no business using are refused before the kernel acts on them.",
    "def": "Every interaction between a program and the kernel is a system call. Seccomp lets you attach a filter to a process: a small program the kernel runs on each system call to decide whether to allow it, fail it with an error, or kill the process. Filters are inherited by children and cannot be removed once installed. It exists to shrink the kernel's attack surface: a bug in an obscure system call cannot be exploited by a process that is not allowed to call it. Docker applies a default profile to every container, and <code>--security-opt seccomp=unconfined</code> or <code>--privileged</code> switches it off. In a transcript, a blocked call usually surfaces as a baffling <q>Operation not permitted</q> from a command running as root; <code>Seccomp:</code> in <code>/proc/self/status</code> tells you whether a filter is active. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a>.",
    "also": "seccomp-bpf, secure computing mode",
    "see": [
      "system-call",
      "capability",
      "attack-surface",
      "gvisor",
      "apparmor"
    ]
  },
  "no-new-privileges": {
    "name": "no-new-privileges",
    "short": "A per-process kernel flag that guarantees the process and all its descendants can never gain more privileges than they have now, which neutralises setuid programs such as sudo.",
    "def": "Normally, executing a program can <em>raise</em> privilege: a setuid-root binary like <code>sudo</code> or <code>su</code> runs as root whoever launches it, and files can carry capabilities too. The <code>no_new_privs</code> flag turns that off. Once set on a process it is inherited by every child and cannot be unset, and from then on <code>execve</code> ignores setuid bits and file capabilities. It exists so that a confined process cannot climb out through some privileged helper that happens to be installed. In Docker you set it with <code>--security-opt no-new-privileges</code>. It matters for evals because running the agent as a non-root user is only a real restriction if there is no route back to root, and a stray setuid binary in the task image is such a route. Check <code>NoNewPrivs:</code> in <code>/proc/self/status</code>. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a> and <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "no_new_privs, PR_SET_NO_NEW_PRIVS",
    "see": [
      "setuid",
      "privilege-escalation",
      "sudo",
      "capability",
      "seccomp"
    ]
  },
  "apparmor": {
    "name": "AppArmor",
    "short": "A Linux security module, enabled by default on Ubuntu, that confines a program to a profile listing the files, capabilities, and network access it may use, even when it runs as root.",
    "def": "Ordinary Unix permissions are discretionary: the owner of a file decides who may touch it, and root bypasses the lot. AppArmor adds <em>mandatory</em> access control: a per-program profile, loaded into the kernel, lists which paths may be read, written, or executed and which capabilities may be used, and the kernel enforces it regardless of user ID. It exists as a backstop: if a confined program is compromised, it still cannot reach outside its profile. On hosts where AppArmor is enabled, Docker applies a default profile (<code>docker-default</code>) to containers. You will mostly meet it as a puzzle: an operation fails with <q>Permission denied</q> although the permission bits and capabilities say it should work, and the explanation is a denial recorded in the host's kernel log. Red Hat-family systems use SELinux for the same job. See <a href='pages/21-cgroups-capabilities-seccomp.html'>Cgroups, Capabilities, and Seccomp</a>.",
    "also": "LSM, mandatory access control",
    "see": [
      "seccomp",
      "capability",
      "permission-bits",
      "dmesg",
      "privileged-container"
    ]
  },
  "privileged-container": {
    "name": "Privileged Container",
    "short": "A container started with docker run --privileged, which switches off most of Docker's protections: all capabilities granted, seccomp and AppArmor disabled, host devices exposed.",
    "def": "<code>--privileged</code> is a single flag that undoes the restrictions that make a container a sandbox. Per Docker's reference, it enables all kernel capabilities, disables the default seccomp and AppArmor profiles, grants access to all host devices, and makes <code>/sys</code> and the cgroup mounts read-write. Docker's documentation is blunt: a privileged container <q>is not a securely sandboxed process</q> and can take control of the host. The flag exists for special cases like running Docker inside Docker, and it spreads because it makes confusing permission errors go away. For an eval it means the namespaces still give the agent a separate <em>view</em>, but almost nothing stops it acting on the host. Check with <code>docker inspect --format '{{.HostConfig.Privileged}}'</code>, and treat <code>true</code> on an agent's container as a finding. This course uses the flag only on throwaway lab containers. See <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "--privileged",
    "see": [
      "capability",
      "seccomp",
      "apparmor",
      "container-escape",
      "least-privilege"
    ]
  },
  "rootless": {
    "name": "Rootless",
    "short": "A way of running the container engine itself, and every container it starts, as an ordinary non-root user, using user namespaces, so that a breakout does not land as root on the host.",
    "def": "In the default Docker setup the daemon runs as root, so anything that subverts the daemon or escapes a container arrives with root's powers. Rootless mode runs both the daemon and the containers inside a user namespace owned by an unprivileged user: <q>root</q> in the container maps to that user on the host. It exists to limit the damage of a vulnerability in the daemon or the runtime. It is distinct from merely running the container's process as a non-root user (<code>USER</code> in a Dockerfile, <code>--user</code>), which is also worth doing but leaves the daemon privileged. Podman can run this way too. The trade-offs are practical ones, mainly around networking and some storage and resource-limit features, which is why many eval setups still run rootful Docker and rely on the hardening flags instead. See <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>.",
    "also": "rootless mode, rootless Docker",
    "see": [
      "user-namespace",
      "docker-daemon",
      "root-user",
      "least-privilege",
      "container-escape"
    ]
  },
  "container-escape": {
    "name": "Container Escape",
    "short": "Any way a process inside a container gains access to the host or to other containers, defeating the isolation the container was supposed to provide.",
    "def": "In practice escapes come in two kinds. The common kind is misconfiguration: a mounted Docker socket, <code>--privileged</code>, a broad capability like <code>CAP_SYS_ADMIN</code>, a bind mount of a sensitive host directory, shared host namespaces. No exploit is needed; the door was left open. The rare kind is a genuine vulnerability in the kernel or the container runtime, which matters because every container shares the host kernel. This course teaches you to check for and close the first kind, and to choose a stronger boundary (gVisor, a microVM) when the second kind is within your threat model. For evals the concern is concrete: the harness, the grader, other tasks' answers, and API keys usually live on the host side. See <a href='pages/23-hardening-containers.html'>Locking Down a Container</a> and <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "container breakout, sandbox escape",
    "see": [
      "docker-socket",
      "privileged-container",
      "attack-surface",
      "isolation",
      "threat-model"
    ]
  },
  "chroot": {
    "name": "chroot",
    "short": "A command and system call that changes which directory a process treats as / (the root of its filesystem); an ancestor of containers, but not a security boundary on its own.",
    "def": "<code>chroot /some/dir command</code> runs a command with <code>/some/dir</code> as its root directory, so <code>/bin/sh</code> resolves to <code>/some/dir/bin/sh</code> and paths above it are unreachable by name. It exists for practical jobs like repairing an installed system from a rescue disk or building software against a different set of libraries. It is the oldest idea behind containers, <q>give the process a different filesystem tree</q>, but the man page is explicit that it changes one ingredient of path resolution and is not intended for security: a root process can get out, and nothing else (processes, network, users) is isolated at all. Containers use mount namespaces and <code>pivot_root</code> instead. Knowing this lets you evaluate a sandbox that claims isolation by <code>chroot</code> alone: it is a convenience, not a wall. See <a href='pages/20-namespaces.html'>Namespaces: What a Container Really Is</a>.",
    "also": "chroot jail",
    "see": [
      "root-directory",
      "mount-namespace",
      "namespace",
      "isolation"
    ]
  },
  "oci": {
    "name": "OCI",
    "short": "The Open Container Initiative: the industry standards body whose specifications define what a container image is and how a runtime must run it, so tools from different vendors interoperate.",
    "def": "The Open Container Initiative publishes the specifications that make <q>a container</q> a portable thing and not a Docker-only format. The image specification defines how layers and config are packaged; the runtime specification defines the bundle (a root filesystem plus a <code>config.json</code> listing namespaces, mounts, capabilities, cgroup limits) that a low-level runtime turns into a running process; the distribution specification covers how registries serve images. The standards exist so that an image built with one tool runs under another. This is what makes the isolation ladder practical for evals: because runtimes such as runc and gVisor's <code>runsc</code> both implement the OCI runtime interface, you can keep the same task images and the same harness and swap only the runtime underneath to get a stronger boundary. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a> and <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a>.",
    "also": "Open Container Initiative",
    "see": [
      "runc",
      "container-runtime",
      "image",
      "gvisor",
      "registry"
    ]
  },
  "runc": {
    "name": "runc",
    "short": "The standard low-level container runtime: the small program that actually creates the namespaces and cgroups and starts the container's process, following the OCI runtime specification.",
    "def": "When you type <code>docker run</code>, Docker does not create the container itself. The daemon hands the job down a chain (dockerd, then containerd, then runc), and runc is the piece at the bottom that makes the system calls: create the namespaces, apply the cgroup limits, drop capabilities, install the seccomp filter, pivot into the image's filesystem, and <code>exec</code> your command. It is the reference implementation of the OCI runtime specification and Docker's default. It earns a glossary entry because it is the swappable part: <code>docker run --runtime=runsc</code> replaces it with gVisor, and other runtimes start a small VM instead, with no change to the image. When someone asks what isolates the agent, <q>runc</q> means <q>namespaces and a shared kernel</q>. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "see": [
      "container-runtime",
      "oci",
      "docker-daemon",
      "gvisor",
      "namespace"
    ]
  },
  "container-runtime": {
    "name": "Container Runtime",
    "short": "The software that turns an image into a running, isolated process; the choice of runtime (runc, gVisor, a microVM-based runtime) decides how strong the sandbox boundary is.",
    "def": "<q>Container runtime</q> is used at two levels. High-level runtimes such as containerd manage images, storage, and container lifecycles. Low-level runtimes do the actual isolating: runc sets up namespaces and cgroups around a process on the shared host kernel; gVisor's <code>runsc</code> puts a user-space kernel between the process and the host; Kata-style runtimes boot a lightweight virtual machine per container. Because they all speak the OCI interface, the layer above does not care which is in use. For an evals engineer this is the most consequential single setting in the stack that nobody looks at. Two labs can run the same benchmark from the same images with very different exposure if one uses the default runtime and the other a sandboxed one. <code>docker info</code> lists the configured runtimes and the default. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder: Containers, gVisor, MicroVMs</a>.",
    "also": "OCI runtime",
    "see": [
      "runc",
      "gvisor",
      "oci",
      "microvm",
      "isolation"
    ]
  },
  "gvisor": {
    "name": "gVisor",
    "short": "An open-source sandbox that runs containers on top of its own user-space 'application kernel', which intercepts their system calls so they never talk to the host kernel directly.",
    "def": "A normal container's system calls go straight to the host kernel it shares with everything else. gVisor inserts a layer: in its documentation's words, it is <q>an application kernel that implements a Linux-like interface</q>, which <q>intercepts application system calls and acts as the guest kernel, without the need for translation through virtualized hardware</q>. The component that does this is called the Sentry; file access goes through a separate host process, the Gofer. It ships an OCI runtime, <code>runsc</code>, that integrates with Docker and Kubernetes, so existing images run with <code>--runtime=runsc</code>. The documented price is <q>reduced application compatibility and higher per-system call overhead</q>. In eval terms: a stronger boundary for untrusted agent code, at the risk that some task's software behaves differently or runs slower than under runc, which you must rule out first. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "runsc",
    "see": [
      "container-runtime",
      "system-call",
      "seccomp",
      "microvm",
      "attack-surface"
    ]
  },
  "microvm": {
    "name": "MicroVM",
    "short": "A stripped-down virtual machine, with its own guest kernel but only a handful of emulated devices, designed to start quickly and cheaply enough to be used like a container.",
    "def": "A microVM is a real virtual machine reduced to the minimum. It boots its own Linux kernel under hardware virtualization, so the workload's system calls hit the <em>guest's</em> kernel and not the host's, but it drops the legacy hardware a general-purpose VM emulates, leaving little more than a network device, a disk, and a console. It exists to answer a specific trade-off: containers are fast but share a kernel; traditional VMs have a strong boundary but are heavy. Firecracker, whose documentation says microVMs combine the isolation of VMs with <q>the speed and resource efficiency of containers</q>, is the best-known implementation. For running code written by an agent you do not trust, on hosts shared with other tenants or with your secrets, this is the top rung of the ladder. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder: Containers, gVisor, MicroVMs</a>.",
    "also": "micro virtual machine",
    "see": [
      "firecracker",
      "virtual-machine",
      "kvm",
      "hypervisor",
      "isolation"
    ]
  },
  "firecracker": {
    "name": "Firecracker",
    "short": "An open-source virtual machine monitor from Amazon Web Services that uses Linux KVM to create and manage microVMs with a deliberately minimal set of emulated devices.",
    "def": "Firecracker describes itself as <q>an open source virtualization technology purpose-built for creating and managing secure, multi-tenant container and function-based services</q>, built at Amazon Web Services for services such as AWS Lambda. It <q>runs in user space and uses the Linux Kernel-based Virtual Machine (KVM) to create microVMs</q>. Its security argument is subtraction: only a few emulated devices (virtio network, block, and vsock devices, a serial console, a minimal keyboard controller), so there is little device-emulation code for a guest to attack, plus a companion program, the <code>jailer</code>, that confines the Firecracker process itself as a second line of defence. It also supports snapshots that save guest memory and emulated hardware state so a microVM can be resumed later. When a sandbox vendor says your agent runs in a <q>microVM</q>, this is the kind of technology meant. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "see": [
      "microvm",
      "kvm",
      "hypervisor",
      "snapshot",
      "tenancy"
    ]
  },
  "hypervisor": {
    "name": "Hypervisor",
    "short": "The software layer that creates and runs virtual machines, giving each guest operating system the illusion of its own hardware while keeping guests separated from each other and from the host.",
    "def": "A hypervisor (or virtual machine monitor) sits between physical hardware and guest operating systems. It uses CPU virtualization features to let each guest kernel run at near-native speed while trapping the operations that would let one guest affect another, and it presents virtual devices (disk, network card) in place of the real ones. It exists so that many mutually distrusting systems can share one physical machine; it is the foundation of every cloud. On Linux the kernel itself becomes the hypervisor through KVM, with a user-space program such as QEMU or Firecracker supplying the devices. The contrast that matters for sandboxing: the interface a guest sees is a small set of virtual hardware, whereas the interface a container sees is the entire Linux system-call surface. A narrower interface means fewer places for a boundary-crossing bug. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "virtual machine monitor, VMM",
    "see": [
      "virtual-machine",
      "kvm",
      "microvm",
      "attack-surface",
      "isolation"
    ]
  },
  "kvm": {
    "name": "KVM",
    "short": "Kernel-based Virtual Machine: the part of the Linux kernel that uses the CPU's hardware virtualization support to run virtual machines, exposed to programs as the device /dev/kvm.",
    "def": "KVM turns the Linux kernel into a hypervisor. It does not emulate a computer by itself; it exposes the CPU's virtualization extensions through the device file <code>/dev/kvm</code>, and a user-space program (QEMU, Firecracker) opens that file to create a VM, give it memory, and run guest code directly on the processor. The user-space program supplies the virtual devices. The split exists so that the performance-critical, hardware-specific part lives in the kernel once, and different VM monitors can build on it. Practical consequence for evals infrastructure: microVM sandboxes need <code>/dev/kvm</code>, and if your harness itself runs inside a cloud VM, that requires nested virtualization, which not every cloud instance type offers. Checking whether <code>/dev/kvm</code> exists is the first step in finding out which rungs of the isolation ladder a host can support. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "Kernel-based Virtual Machine",
    "see": [
      "hypervisor",
      "virtual-machine",
      "firecracker",
      "microvm",
      "device-file"
    ]
  },
  "virtual-machine": {
    "name": "Virtual Machine",
    "short": "A complete emulated computer, with its own kernel, memory, disks, and network card, running as a guest on a physical host under the control of a hypervisor.",
    "def": "A virtual machine is a software-defined computer. It boots its own operating system kernel, which believes it owns the hardware; the hypervisor underneath maps that virtual hardware onto a share of the real thing. This is the key difference from a container, which is only a process on the <em>host's</em> kernel. A VM costs more (memory for a second kernel, seconds to boot, a disk image to manage) and buys a stronger, narrower boundary plus a kernel of your own, which the systemd and firewall labs need. You are already using one: Docker Desktop on a Mac runs all containers inside a hidden Linux VM. Cloud instances are VMs too, so a typical eval stack is containers inside a VM, and knowing which layer a setting belongs to saves hours of confusion. See <a href='pages/01-lab-setup.html'>Lab Setup</a> and <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "VM, guest",
    "see": [
      "hypervisor",
      "kvm",
      "microvm",
      "container",
      "kernel"
    ]
  },
  "snapshot": {
    "name": "Snapshot",
    "short": "A saved point-in-time copy of an environment's state (a disk, or a whole VM including memory) that can be restored later to get back exactly that state.",
    "def": "A snapshot freezes state so you can return to it. A disk snapshot captures the filesystem; a full VM snapshot also captures memory and device state, so the restored machine continues mid-thought with its processes still running. Firecracker, for instance, documents snapshots that save guest memory and emulated hardware state and can be loaded into a new process to resume the guest. Container images play the same role for filesystems only: every container starts from the image's frozen layers. Snapshots are how evals get a clean, identical starting line cheaply: prepare the environment once (install, warm up, seed the database), snapshot it, and restore per attempt. The caveat is that a snapshot faithfully preserves mistakes too, and restored memory state can duplicate things meant to be unique, such as random seeds or clocks. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "checkpoint",
    "see": [
      "reset",
      "virtual-machine",
      "firecracker",
      "image",
      "nondeterminism"
    ]
  },
  "attack-surface": {
    "name": "Attack Surface",
    "short": "Everything an untrusted party can reach and interact with: every interface, service, file, and system call through which a flaw could be triggered. Less surface means fewer ways in.",
    "def": "Attack surface is a way of counting exposure without knowing where the bugs are. You cannot list the vulnerabilities in a kernel, but you can list what the untrusted code is able to touch: which system calls it may make, which devices it sees, which sockets and mounted files it can open, which network services answer it. Every hardening step in this course is a surface reduction: dropping capabilities, a seccomp filter, a read-only root filesystem, <code>--network none</code>, not mounting the Docker socket. It is also the honest way to compare isolation technologies: a container faces the host kernel's whole system-call interface; a microVM guest faces a few virtual devices. For an agent sandbox, include the eval-specific surface too: files that reveal answers, credentials in environment variables, reachable graders. See <a href='pages/23-hardening-containers.html'>Locking Down a Container</a> and <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "see": [
      "threat-model",
      "trust-boundary",
      "seccomp",
      "least-privilege",
      "isolation"
    ]
  },
  "threat-model": {
    "name": "Threat Model",
    "short": "An explicit statement of what you are protecting, from whom, and what that adversary is assumed able to do; the basis for deciding how much isolation is enough.",
    "def": "A threat model answers three questions before you pick any technology: what could go wrong, who or what would cause it, and what are they capable of? For an agent sandbox the usual candidates are: the agent damaging the host by accident (a stray <code>rm -rf</code>, a fork bomb); the agent gaming the eval by reading answers or editing tests; model-written code reaching the internet or your cloud credentials; and, at the far end, a capable model deliberately trying to break out. A hardened container handles the first few well. The last, or running strangers' tasks next to your secrets, argues for gVisor or a microVM. Writing the model down also tells auditors what you did <em>not</em> defend against, which is part of reporting a result honestly. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "see": [
      "attack-surface",
      "trust-boundary",
      "isolation",
      "tenancy",
      "environment-integrity"
    ]
  },
  "trust-boundary": {
    "name": "Trust Boundary",
    "short": "A line in a system where data or control passes between parts trusted to different degrees; whatever crosses it must be checked, because the less-trusted side may be hostile or wrong.",
    "def": "A trust boundary separates components you rely on from components you do not. In an agentic eval the central one runs between the harness (your code, holding API keys, the answer key, and the scorer) and the sandbox (where model-generated commands run). Everything crossing that line deserves suspicion in both directions. Inward: mounts, environment variables, and network routes are all things you handed the agent; a read-write mount of the tests directory moves the grader to the wrong side of the line. Outward: the files and output the harness reads back were produced by the untrusted side, so a scorer that trusts a <code>results.json</code> written inside the sandbox is trusting the agent's own report of its grade. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity: Where Cheating Lives</a>.",
    "see": [
      "threat-model",
      "attack-surface",
      "harness",
      "sandbox",
      "test-tampering"
    ]
  },
  "isolation": {
    "name": "Isolation",
    "short": "The degree to which a workload is prevented from seeing, affecting, or being affected by anything outside it; a matter of degree and of which resources, not a yes/no property.",
    "def": "Isolation is not one thing, so <q>is it isolated?</q> is the wrong question. Ask: isolated <em>with respect to what</em>? Filesystem (what is mounted, read-only or not), processes (PID namespace), network (what it can reach), resources (cgroup limits), privileges (user, capabilities, seccomp), and the kernel itself (shared, intercepted, or separate). Different technologies sit at different points: a bare process, a hardened container, a gVisor sandbox, a microVM, a separate physical machine. This course calls that the isolation ladder; each rung costs more and shares less. Evals need isolation for two distinct reasons that are worth keeping apart: <em>safety</em> (the agent cannot harm the host or reach secrets) and <em>validity</em> (runs cannot contaminate each other and the agent cannot reach the answers). A setup can be strong on one and weak on the other. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a> and <a href='pages/20-namespaces.html'>Namespaces</a>.",
    "see": [
      "namespace",
      "sandbox",
      "container-runtime",
      "threat-model",
      "tenancy"
    ]
  },
  "tenancy": {
    "name": "Tenancy",
    "short": "Who shares a piece of infrastructure with whom: single-tenant means one owner's workloads per host or kernel; multi-tenant means mutually distrusting workloads run side by side.",
    "def": "A tenant is a party whose workloads should not be able to see or disturb another's. Tenancy describes the sharing arrangement: one tenant per physical host, per VM, per kernel, or many tenants on a shared kernel. The idea transfers directly to evals. Running forty task containers in parallel on one host makes each task a tenant of the same kernel, the same disk, and often the same Docker network: a task that fills the disk or saturates the CPU changes its neighbours' results, and containers on a shared bridge may be able to reach each other. If the host also holds your API keys or the answer keys, the harness is a tenant too. Decide the tenancy first, then the isolation rung. See <a href='pages/24-isolation-ladder.html'>The Isolation Ladder</a>.",
    "also": "multi-tenancy, single-tenant",
    "see": [
      "isolation",
      "threat-model",
      "cgroup",
      "microvm",
      "bridge-network"
    ]
  },
  "eval": {
    "name": "Eval",
    "short": "A repeatable test that measures how well an AI system performs a task, by running it on a fixed set of inputs and scoring the results.",
    "def": "An eval (short for evaluation) is a repeatable measurement of how well an AI system does something: run the system on a fixed set of tasks, score each result, and aggregate the scores into a number you can track and compare. Evals exist because you cannot tell whether a change helped by eyeballing a few outputs. This course is about the kind where the system under test is an agent acting inside a Linux box. There, the measuring instrument is not just a dataset and a scoring rule; it includes a container image, a network policy, resource limits, timeouts, and a harness that drives it all. If any of those is misconfigured, the number measures the misconfiguration. That is the argument for learning Linux as an evals engineer, made in full in <a href='pages/00-orientation.html'>Orientation: Why Linux, for Evals</a>.",
    "also": "evaluation",
    "see": [
      "benchmark",
      "harness",
      "environment",
      "scorer",
      "agent"
    ]
  },
  "benchmark": {
    "name": "Benchmark",
    "short": "A standardized, published eval, with fixed tasks and fixed scoring rules, that lets different models or agents be compared on the same footing.",
    "def": "A benchmark is an eval that has been standardized and published so anyone can run it and compare results: a fixed set of tasks and fixed scoring rules. Standardization is the whole point; numbers from different task sets or rules cannot be compared. For an agentic benchmark, <q>fixed</q> has to cover far more than the questions. Physically, the benchmark is a pile of Linux environments, usually one container image per task, plus a harness and test scripts. If the images are rebuilt from unpinned packages, if one lab runs with internet access and another without, or if time and memory limits differ, the labs are running different benchmarks under the same name. Reading a benchmark therefore means reading its Dockerfiles and harness configuration, not just its paper. See <a href='pages/00-orientation.html'>Orientation</a> and <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "see": [
      "eval",
      "task-image",
      "harness",
      "swe-bench",
      "terminal-bench"
    ]
  },
  "agent": {
    "name": "Agent",
    "short": "An LLM-powered system that works toward a goal over many steps, choosing actions such as running shell commands, observing the results, and deciding what to do next.",
    "def": "An agent is a language model wrapped in a loop: it reads the situation, picks an action (usually a tool call), sees the result, and repeats until it finishes or gives up. Agents exist because real tasks, like fixing a bug or configuring a server, cannot be done in one reply; they require acting and reacting. In the evals this course covers, the action is nearly always <q>run this command in a Linux shell</q>. From the operating system's point of view the agent is a user at a terminal: an unusually fast one, with no intuition about what is dangerous and no ability to press <kbd>Ctrl</kbd>+<kbd>C</kbd> when a command hangs. Everything you learn about permissions, processes, and networks applies to it as it would to any user you did not fully trust. See <a href='pages/00-orientation.html'>Orientation</a> and <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "see": [
      "tool-call",
      "bash-tool",
      "trajectory",
      "sandbox",
      "harness"
    ]
  },
  "harness": {
    "name": "Harness",
    "short": "The software that runs an eval end to end: it starts each task's environment, passes the agent's actions in and results out, enforces limits, runs the scorer, and records everything.",
    "def": "A harness is the program that turns a benchmark into results. For a simple eval it loads inputs, calls the model, and scores the outputs. For an agentic eval it is also a systems orchestrator: it builds or pulls the task image, starts the container with the right mounts, network, and limits, relays each command the model requests (typically via <code>docker exec</code> or an equivalent), captures stdout, stderr, and the exit status, enforces timeouts, runs the verifier, tears everything down, and writes the log. It is also where many scoring errors originate, because each of those steps is ordinary Linux plumbing that can be wrong: a captured stream dropped, a timeout that kills the wrong process, a container reused between tasks. Inspect is an example of a harness. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "evaluation framework, eval harness",
    "see": [
      "sandbox",
      "bash-tool",
      "timeout",
      "scorer",
      "inspect"
    ]
  },
  "sandbox": {
    "name": "Sandbox",
    "short": "An isolated, disposable execution environment, usually a container or VM, where an agent can run commands and change files without affecting anything real.",
    "def": "A sandbox is a walled-off machine for the agent to work in: typically a Docker container, sometimes a gVisor sandbox or a microVM. Evals need one for two reasons. Safety: the agent runs arbitrary model-written commands, which you do not want touching your laptop, your cloud account, or the harness. Reproducibility: every attempt starts from the same clean state, so results are comparable. The word names an intent, not a guarantee. A container with the Docker socket mounted, <code>--privileged</code> set, or unrestricted internet is called a sandbox in somebody's config file right now. This course's job is to let you check the claim: what is mounted, which user the agent runs as, which capabilities it holds, what it can reach over the network, what limits apply. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>, <a href='pages/23-hardening-containers.html'>Locking Down a Container</a>, and <a href='pages/28-ten-minute-audit.html'>The Ten-Minute Audit</a>.",
    "see": [
      "container",
      "isolation",
      "environment",
      "harness",
      "egress"
    ]
  },
  "environment": {
    "name": "Environment",
    "short": "The world an agent acts in during an eval; in this course, a Linux system with its files, users, running processes, installed packages, and network access.",
    "def": "The environment is everything the agent can act on and observe. Agent benchmarks differ from question-answering ones chiefly in that they must ship an environment, not just questions. In this course's territory that means a Linux box: a filesystem with the task's repository or data, particular package versions, a user account the agent runs as, perhaps background services, and a network that reaches some things and not others. The environment is part of the measuring instrument. A missing tool, a stale package index, a full disk, or a reachable answer key changes the score without any change in the model's ability, and a too-forgiving environment quietly measures the wrong thing. (Do not confuse this with <em>environment variables</em>, a separate Linux concept with its own entry.) See <a href='pages/00-orientation.html'>Orientation</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "task environment",
    "see": [
      "sandbox",
      "task-image",
      "environment-integrity",
      "agent",
      "reset"
    ]
  },
  "trajectory": {
    "name": "Trajectory",
    "short": "The full step-by-step record of one agent run: every model message, every tool call, and every result that came back, in order.",
    "def": "A trajectory is the complete sequence of what an agent did in one attempt: each piece of reasoning, each tool call, each observation returned. It matters because the final pass or fail says almost nothing about <em>why</em>; the information is in the steps. In a Linux-sandbox eval a trajectory is, in substance, a terminal session: commands, their output, their exit codes. Reading one well is a Linux skill. <code>command not found</code> (exit 127) means a missing package or a <code>PATH</code> problem; <code>Permission denied</code> points at the user the agent runs as; a step that returns nothing until the timeout fires is often a program waiting for keyboard input. These distinguish a model that could not do the task from an environment that would not let it. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "trace, episode",
    "see": [
      "transcript",
      "tool-call",
      "rollout",
      "error-analysis",
      "exit-status"
    ]
  },
  "transcript": {
    "name": "Transcript",
    "short": "The logged, human-readable record of an agent run, showing the commands it issued and the terminal output it received; the primary evidence for understanding a result.",
    "def": "A transcript is the trajectory as written down by the harness: the text you actually open when you want to know what happened. In terminal-based evals it shows each command, the captured output, and usually the exit status and timing. Two cautions make this a Linux topic. First, a transcript shows only what the harness captured. If it recorded stdout but not stderr, error messages are absent; if output was truncated at a size limit, the decisive line may be gone; if the agent drove a full-screen program, you may see raw escape sequences. Second, the transcript is the agent's-eye view, which can differ from the truth: a command can report success inside a sandbox whose network was silently blocked. When a transcript and a score disagree, check the environment. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a> and <a href='pages/04-streams-pipes-redirection.html'>Streams, Pipes, and Redirection</a>.",
    "also": "log, terminal transcript",
    "see": [
      "trajectory",
      "stderr",
      "error-analysis",
      "tty",
      "infrastructure-failure"
    ]
  },
  "tool-call": {
    "name": "Tool Call",
    "short": "A single action an agent takes on the outside world, such as running a shell command, requested by the model in structured form and executed on its behalf by the harness.",
    "def": "A tool call is how a model acts instead of only talking: it emits a structured request (<q>run <code>ls -la /app</code></q>), the surrounding program executes it, and the result is fed back into the model's context. The model never touches the machine; the harness does, which means each call passes through Linux plumbing you can reason about. For a shell tool, the harness starts a process in the sandbox, as some user, in some working directory, with some environment variables, waits up to some timeout, and collects stdout, stderr, and the exit status. Each <q>some</q> is a harness design decision that shapes what the agent experiences: whether <code>cd</code> persists between calls, whether a background process survives, what happens to a command that prompts for input. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "function call, action",
    "see": [
      "bash-tool",
      "agent",
      "harness",
      "trajectory",
      "exit-status"
    ]
  },
  "bash-tool": {
    "name": "Bash Tool",
    "short": "The tool a harness gives an agent for running shell commands inside the sandbox; the model supplies a command string and gets back the output and exit status.",
    "def": "The bash tool is the agent's hands. The model supplies a command string; the harness runs it with a shell inside the sandbox and returns what was printed. Inspect, for example, ships a <code>bash()</code> tool that executes its commands in the sample's sandbox. It is simple to describe and full of consequences. Usually there is no terminal attached, so programs that expect one (pagers, editors, <code>sudo</code> password prompts, <code>apt</code> asking <q>[Y/n]</q>) hang until the timeout. In many implementations each call is a fresh shell, so <code>cd</code> and <code>export</code> do not carry over. Output may be truncated. The command runs as whichever user the harness chose. Much of what looks like strange agent behaviour in a transcript is a sensible reaction to these constraints. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a> and <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "shell tool, execute tool",
    "see": [
      "tool-call",
      "bash",
      "interactive-prompt",
      "tty",
      "timeout"
    ]
  },
  "task-image": {
    "name": "Task Image",
    "short": "The container image that defines one benchmark task's starting environment: the operating system, installed tools, and the task's files, exactly as the agent will find them.",
    "def": "In container-based benchmarks each task (or family of tasks) ships with an image: a base distribution, the dependencies at specific versions, and the task's materials, such as a repository checked out at the right commit. The task image is what makes a task reproducible, since every attempt by every model starts from the same bytes. It is also where environment bugs are baked in. Audit one the way this course teaches: which base and is it pinned by digest; which user does it run as; is it Alpine, where the agent's assumptions about <code>bash</code> and GNU tools fail; what is in the layer history; does the filesystem contain anything the agent should not see, such as tests, solutions, or git history from the future; were credentials used at build time left behind? See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "see": [
      "image",
      "dockerfile",
      "base-image",
      "environment",
      "solution-leakage"
    ]
  },
  "verifier": {
    "name": "Verifier",
    "short": "The script or test suite that checks, after the agent finishes, whether the task was actually accomplished, usually by running tests or inspecting the final state of the sandbox.",
    "def": "A verifier is the task-specific check that decides success: run the unit tests, confirm the service answers on its port, compare a file against the expected content. Terminal-Bench, for instance, describes each task as including <q>a test script to verify if the language model / agent completed the task successfully</q>. It exists because in agentic tasks there is no single right output string to compare against; success is a property of the world the agent left behind. A verifier is a program, so the course's concerns apply. Its verdict usually travels as an exit status, so a verifier that crashes must not be read as <q>tests failed</q>. If it runs inside the agent's container, the agent could have altered what it runs. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "test script, checker, grader",
    "see": [
      "scorer",
      "held-out-tests",
      "test-tampering",
      "exit-status",
      "flaky-test"
    ]
  },
  "scorer": {
    "name": "Scorer",
    "short": "The component of an eval harness that turns the result of one attempt into a grade, by exact match, by running checks, or by asking a model to judge.",
    "def": "A scorer is the grading half of a harness: it takes what an attempt produced and emits a verdict, pass/fail or a number, which is then aggregated into the headline metric. The term is Inspect's, where a scorer <q>evaluates the output—using text comparisons, model grading, or other custom schemes</q>, but every framework has the role. In sandbox evals the scorer typically reaches into the environment: it executes the verifier or reads files from the container, then maps the outcome to a score. That mapping is where Linux details corrupt results silently. Exit code 137 (killed, often by the OOM killer), 124 (timed out), and 1 (tests failed) are three different stories; a scorer that collapses them all to <q>fail</q> counts infrastructure problems as model failures. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a> and <a href='pages/10-signals-exit-codes.html'>Signals, Exit Codes, and Timeouts</a>.",
    "also": "grader",
    "see": [
      "verifier",
      "harness",
      "exit-status",
      "infrastructure-failure",
      "state-based-evaluation"
    ]
  },
  "oracle-solution": {
    "name": "Oracle Solution",
    "short": "A known-correct reference solution shipped with a benchmark task, used to prove the task is solvable and the verifier works, and which must never be visible to the agent.",
    "def": "An oracle (or reference, or gold) solution is the benchmark author's own answer to a task: a script of commands or a patch that, applied to the fresh environment, makes the verifier pass. Terminal-Bench tasks include <q>a reference (“oracle”) solution that solves the task</q>; SWE-bench's dataset carries a gold patch for each instance. It exists for quality control. Running the oracle through the real harness shows that the task is solvable, the environment builds, and the tests can pass at all; when the oracle fails, the task is broken, not the model. That makes it the best single smoke test after any infrastructure change. The obligation it creates is secrecy: the file must not be copied into the task image, left in an earlier layer, mounted into the sandbox, or recoverable from version-control history. See <a href='pages/26-environment-integrity.html'>Environment Integrity: Where Cheating Lives</a>.",
    "also": "reference solution, gold patch, answer key",
    "see": [
      "solution-leakage",
      "verifier",
      "task-image",
      "layer",
      "infrastructure-failure"
    ]
  },
  "held-out-tests": {
    "name": "Held-Out Tests",
    "short": "Grading tests that are kept outside the sandbox while the agent works and only brought in afterwards, so the agent can neither read them nor change them.",
    "def": "Held-out tests are a defence built from one observation: an agent cannot tamper with or overfit to a file that does not exist in its filesystem. The task image contains the problem but not the grading tests; when the agent is finished, the harness copies the tests in (or copies the agent's work out to a clean container) and runs them. The alternative, leaving the tests in the working directory and hoping, invites both innocent and deliberate failure: agents edit failing tests to make them pass, or special-case the exact inputs they can see. Implementing it is pure Linux: check what is present in the image and its layers, keep any test mounts read-only, run the verifier as a different user or in a fresh container, and restore any test files the agent's work overlaps. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "hidden tests",
    "see": [
      "test-tampering",
      "verifier",
      "read-only-mount",
      "environment-integrity",
      "reward-hacking"
    ]
  },
  "reward-hacking": {
    "name": "Reward Hacking",
    "short": "When an agent gets a passing score by exploiting a flaw in how success is measured, instead of doing the task the measurement was meant to capture.",
    "def": "A score is a proxy for what you care about, and an optimizer pushed against a proxy finds the gaps. Reward hacking (also called specification gaming) is an agent satisfying the letter of the check and not the intent: editing the tests, hard-coding expected outputs, overwriting the results file, finding the answer on disk or online. The term comes from reinforcement learning. This course treats it as a fact about environments more than about models: most hacks need an opening, and the openings are Linux facts you can inspect. Tests writable by the agent's user, a verifier running inside the agent's container, open egress, leftover solution files. Closing them is environment engineering; detecting what slipped through is transcript reading. A benchmark that ignores this reports cheating as capability. See <a href='pages/26-environment-integrity.html'>Environment Integrity: Where Cheating Lives</a>.",
    "also": "specification gaming, cheating",
    "see": [
      "environment-integrity",
      "test-tampering",
      "solution-leakage",
      "held-out-tests",
      "trust-boundary"
    ]
  },
  "environment-integrity": {
    "name": "Environment Integrity",
    "short": "The property that an eval environment gives the agent no illegitimate route to a passing score and no spurious obstacle to an honest one, so the score reflects the task.",
    "def": "Environment integrity asks whether the sandbox measures what it claims to. It fails in two directions. Too permissive: the answer is reachable (solution files, future git history, the open internet), the grader is editable, or state leaks between attempts, so scores are inflated. Too hostile: a tool is missing, a network dependency is down, a limit is too tight, so scores are deflated by failures that have nothing to do with the model. Both are properties of a Linux system and both are checkable with the tools in this course: <code>findmnt</code> for what is mounted and whether read-only, <code>ls -l</code> and <code>id</code> for who can write what, <code>git log --all</code> for what history is present, <code>ss</code> and <code>curl</code> for what is reachable. Treat it as a checklist you run before trusting a number. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a> and <a href='pages/28-ten-minute-audit.html'>The Ten-Minute Audit</a>.",
    "see": [
      "reward-hacking",
      "solution-leakage",
      "test-tampering",
      "infrastructure-failure",
      "threat-model"
    ]
  },
  "solution-leakage": {
    "name": "Solution Leakage",
    "short": "When a task hands the agent its own answer by accident: in the task description, or in files, image layers, version-control history, or network resources reachable from the sandbox.",
    "def": "Solution leakage is contamination inside a single task: the answer, or a near-complete recipe for it, is available to the agent, so <q>solving</q> becomes retrieval. The sibling course covers the textual form (an issue report that spells out the fix); this course covers the form where the leak is on the machine. A reference solution copied into the image. A file deleted in a later Dockerfile step but still present in an earlier layer. A repository whose <code>.git</code> directory contains the commit that fixed the bug. A package index or website, reachable because egress was left open, that hosts the upstream fix. No memorization is involved, and looking around the filesystem is what a good engineer does. The task is broken, and only an audit of the environment finds it. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "answer leakage",
    "see": [
      "git-history-leak",
      "oracle-solution",
      "layer",
      "egress",
      "environment-integrity"
    ]
  },
  "test-tampering": {
    "name": "Test Tampering",
    "short": "An agent passing a task by altering the thing that grades it: editing or deleting test files, changing the test configuration, or replacing the programs the verifier runs.",
    "def": "If the verifier's inputs live where the agent can write, the agent can change the verdict. The direct form is editing a failing test so it passes, or deleting it. Indirect forms are more Linux-flavoured: adding a config file that makes the test runner skip tests, placing a fake <code>pytest</code> earlier in <code>PATH</code>, or writing the results file the scorer reads. The defences are permissions and boundaries, not instructions. Keep grading tests out of the sandbox until the agent is done, or mount them read-only; run the verifier from a clean container or as a different user; restore known test files before grading; and compare test-file hashes before and after. If the agent runs as root inside the container, file permissions alone stop nothing. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a> and <a href='pages/08-permissions.html'>Permissions and Ownership</a>.",
    "see": [
      "held-out-tests",
      "reward-hacking",
      "read-only-mount",
      "permission-bits",
      "verifier"
    ]
  },
  "git-history-leak": {
    "name": "Git History Leak",
    "short": "Solution leakage through version control: the task's repository still contains commits, branches, tags, or reflog entries from after the bug was fixed, so the agent can read the fix.",
    "def": "Benchmarks built from real repositories check the code out at the commit just before a fix and ask the agent to produce the fix. But a git repository is a database of <em>all</em> its history, and <code>git checkout</code> only changes the working files. If the clone in the task image still holds later commits, the real fix is a query away. The SWE-bench maintainers documented this in their issue tracker: agents used <code>git log --all</code>, which, in their words, <q>leaks future commits that directly fix the issue</q>; their stated mitigation was to remove future repository state and related artifacts (<q>reflogs, branches, origins, tags, and more</q>). The audit is the same commands run defensively inside the task image: <code>git log --all</code>, <code>git branch -a</code>, <code>git tag</code>, <code>git reflog</code>, <code>git remote -v</code>. See <a href='pages/26-environment-integrity.html'>Environment Integrity: Where Cheating Lives</a>.",
    "also": "future commit leak",
    "see": [
      "solution-leakage",
      "swe-bench",
      "task-image",
      "environment-integrity",
      "egress"
    ]
  },
  "flaky-test": {
    "name": "Flaky Test",
    "short": "A test that sometimes passes and sometimes fails on exactly the same code, because its result depends on something uncontrolled like timing, ordering, network, or leftover state.",
    "def": "A flaky test gives different verdicts on identical input. In an eval this is measurement noise injected at the last step: a correct solution is marked wrong, or a wrong one right, by chance. The causes are nearly all environmental. Timing: a test that waits one second for a server to start passes on an idle host and fails when forty containers share the CPU. Network: a test that downloads something fails when the registry or mirror hiccups. Ordering and state: a test that relies on files or ports left by an earlier test. You find flakiness by running the verifier repeatedly against the oracle solution on a loaded machine; a task whose known-good answer does not pass every time should be fixed or dropped before it touches a leaderboard. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a> and <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "flaky verifier, intermittent failure",
    "see": [
      "nondeterminism",
      "verifier",
      "oracle-solution",
      "infrastructure-failure",
      "wall-clock-time"
    ]
  },
  "nondeterminism": {
    "name": "Nondeterminism",
    "short": "Any source of run-to-run variation: the same task and the same model producing different results because of sampling randomness or because the environment was not identical.",
    "def": "Some variation in agent evals is inherent: models sample their outputs, so two attempts differ, which is why results are reported over repeated runs. The rest is environmental, and it is the part you control. Unpinned packages mean Tuesday's image differs from Monday's. Wall-clock timeouts mean a loaded host fails tasks an idle one passes. Live network dependencies change or disappear. Directory listing order, process scheduling, random port assignment, the current date, and hash-seed randomization all vary between runs. State that survives a sloppy reset couples one attempt to the last. The discipline is to remove every source you can (pin by digest, cut the network, set generous and consistent limits, reset completely) so that the variance left over is the model's, and to record the rest (image digests, harness version). See <a href='pages/15-packages-reproducibility.html'>Packages and Reproducible Environments</a> and <a href='pages/26-environment-integrity.html'>Environment Integrity</a>.",
    "also": "run-to-run variance",
    "see": [
      "flaky-test",
      "reproducible-build",
      "version-pinning",
      "reset",
      "rollout"
    ]
  },
  "reset": {
    "name": "Reset",
    "short": "Returning a task environment to its exact initial state before each attempt, normally by destroying the container or VM and creating a fresh one from the image or snapshot.",
    "def": "Every attempt at a task must start from the same state, or attempts are not comparable and one run can leak into the next. With containers the reliable reset is not to clean up but to throw away: remove the container and start a new one from the image,. Inspect's documentation, for example, notes that each sample gets its own sandbox instance so samples do not interfere. What survives a careless reset is the part that lives <em>outside</em> the container's writable layer: named volumes, bind-mounted host directories, a shared database service. Any of these can carry one attempt's work, or damage, into the next. Auditing a reset means listing the mounts and asking of each: is this fresh per attempt? See <a href='pages/22-docker-for-evals.html'>Docker for Eval Environments</a> and <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "environment reset, teardown",
    "see": [
      "snapshot",
      "volume",
      "bind-mount",
      "environment",
      "nondeterminism"
    ]
  },
  "rollout": {
    "name": "Rollout",
    "short": "One complete attempt by an agent at one task, from fresh environment to final verdict; evals typically run many rollouts per task and aggregate them.",
    "def": "A rollout is a single start-to-finish attempt: fresh environment, agent loop until done or out of budget, verification, teardown. The term comes from reinforcement learning; in eval write-ups you will also see <q>attempt</q>, <q>trial</q>, <q>episode</q>, or <q>sample</q>. Because agents are stochastic, serious evals run several rollouts per task, which turns an eval into a throughput problem on real machines. Each rollout costs a container or VM, memory, CPU, disk for its writable layer and logs, and wall-clock time, and running dozens in parallel on one host makes them compete. Overcommit the host and rollouts start failing from timeouts and OOM kills that have nothing to do with the model. Sizing concurrency is part of measurement hygiene. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a> and <a href='pages/12-resources-and-limits.html'>Resources, Limits, and the OOM Killer</a>.",
    "also": "attempt, trial, episode",
    "see": [
      "trajectory",
      "reset",
      "nondeterminism",
      "infrastructure-failure",
      "tenancy"
    ]
  },
  "infrastructure-failure": {
    "name": "Infrastructure Failure",
    "short": "A failed attempt caused by the eval's own machinery (a container that would not start, a network outage, a full disk, a harness bug) and not by the agent's ability.",
    "def": "An infrastructure failure is a rollout that failed for reasons the model had no say in: the image pull was rate-limited, the container was OOM-killed because the limit was set too low, the disk filled with logs, DNS inside the sandbox was broken, the package mirror was down. Scored naively these all look like <q>the agent failed the task</q>, and they depress results unevenly, since they cluster on busy days and heavy tasks. The discipline is to classify before you count. Linux gives you the evidence: exit codes (137, 124, 125 to 127 each mean something specific), <code>dmesg</code> or the journal for OOM kills, <code>docker inspect</code> for a container's final state, <code>df</code> for disk. Infrastructure failures should be retried or excluded and reported separately, never silently merged into the score. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a> and <a href='appendices/b-exit-codes-signals.html'>Appendix B</a>.",
    "also": "infra failure, harness error",
    "see": [
      "error-analysis",
      "failure-mode",
      "exit-status",
      "oom-killer",
      "flaky-test"
    ]
  },
  "inspect": {
    "name": "Inspect",
    "short": "An open-source Python framework for AI evaluations, developed by the UK AI Security Institute and Meridian Labs, with built-in support for running agents' tools inside sandboxes.",
    "def": "Inspect is, in its own documentation's words, <q>a framework for frontier AI evaluations developed by the UK AI Security Institute and Meridian Labs</q>. An eval is assembled from a dataset, a solver, and a scorer. What makes it a recurring example in this course is its sandboxing, which the docs describe as <q>provisioning containers in which tools, agents and scorers can execute commands and code</q>. Docker support is built in, configured with a <code>Dockerfile</code> or a <code>compose.yaml</code>; a <code>local</code> option uses the host's own filesystem with no sandbox; other sandbox types come as extension packages. Standard tools such as <code>bash()</code> run their commands in the sandbox, and your own code can call <code>sandbox().exec()</code>. Each sample gets its own sandbox instance, cleaned up when the task completes. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "Inspect AI, inspect_ai",
    "see": [
      "harness",
      "sandbox",
      "bash-tool",
      "docker-compose",
      "scorer"
    ]
  },
  "terminal-bench": {
    "name": "Terminal-Bench",
    "short": "A benchmark for testing AI agents in real terminal environments, made of a dataset of tasks plus an execution harness that connects a language model to a terminal sandbox.",
    "def": "Terminal-Bench describes itself as <q>the benchmark for testing AI agents in real terminal environments</q>. Per its README it has two parts: <q>a dataset of tasks, and an execution harness that connects a language model to our terminal sandbox</q>. Each task includes an instruction in English, a test script that verifies whether the agent completed the task, and a reference (<q>oracle</q>) solution; running it requires Docker. Its task anatomy illustrates the pattern most agentic benchmarks share: an instruction, a containerized Linux environment, a verifier, and a known-good solution for checking the task itself. The tasks are the everyday work this course teaches, at a command line, so the things that trip agents there (missing tools, interactive prompts, permissions, hung processes) are the things you will learn to recognise. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "also": "T-Bench",
    "see": [
      "benchmark",
      "oracle-solution",
      "verifier",
      "task-image",
      "terminal"
    ]
  },
  "swe-bench": {
    "name": "SWE-bench",
    "short": "A benchmark that tests whether a model can resolve real GitHub issues: given a codebase and an issue, it must produce a patch, which is graded by running the repository's tests in Docker.",
    "def": "SWE-bench is, per its documentation, <q>a benchmark for evaluating large language models on real world software issues collected from GitHub. Given a codebase and an issue, a language model is tasked with generating a patch that resolves the described problem.</q> Evaluation applies the generated patch to the repository and runs the repository's tests, in <q>a containerized Docker environment to ensure consistent results across different platforms</q>; each instance records which tests should go from failing to passing (<code>FAIL_TO_PASS</code>) and which should keep passing (<code>PASS_TO_PASS</code>), and carries a gold patch. For this course it is the standard case study in environment engineering: containerized per-task environments, and a documented integrity problem in which agents could read the fix from the repository's future git history. The sibling course covers its scoring and variants. See <a href='pages/25-how-harnesses-use-linux.html'>page 25</a> and <a href='pages/26-environment-integrity.html'>page 26</a>.",
    "see": [
      "benchmark",
      "git-history-leak",
      "task-image",
      "held-out-tests",
      "oracle-solution"
    ]
  },
  "state-based-evaluation": {
    "name": "State-Based Evaluation",
    "short": "Grading an agent by examining the final state of its environment (files, running services, database contents) against the goal, regardless of the path it took.",
    "def": "State-based evaluation checks the world, not the words: after the agent finishes, the harness examines what is true in the environment and compares it with what the task required. In a Linux sandbox the <q>state</q> is concrete. Does <code>/etc/nginx/nginx.conf</code> contain the right directive, with the right owner and mode? Is a process listening on port 8080 (<code>ss -ltn</code>)? Does <code>curl localhost:8080/health</code> return 200? Is the cron entry installed? This naturally allows many valid paths to the goal and needs no judge model. Its limits are the flip side: it cannot tell a careful run from a destructive one that happened to end in the right place, and it is only as good as the checks. Check too little and a hard-coded shortcut passes; check incidental details and correct solutions fail. See <a href='pages/25-how-harnesses-use-linux.html'>How Harnesses Drive a Sandbox</a>.",
    "see": [
      "outcome-based-evaluation",
      "verifier",
      "environment",
      "scorer",
      "reward-hacking"
    ]
  },
  "outcome-based-evaluation": {
    "name": "Outcome-Based Evaluation",
    "short": "Grading an agent only on whether the end result is correct (do the tests pass?), without judging the steps it took to get there.",
    "def": "Outcome-based evaluation scores the final result and ignores the route: the tests pass or they do not. Its appeal is objectivity; no judge is needed to read a test suite's exit status. Most terminal and coding benchmarks are graded this way. Its blind spot is everything in between, and in a Linux sandbox that blind spot has specific contents. An agent can reach a passing outcome by <code>chmod -R 777</code> on the project, by <code>kill -9</code> on whatever was in its way, by editing the tests, or by fetching the answer from the network, and outcome grading sees only <q>pass</q>. That is why this course pairs outcome scores with two other habits: hardening the environment so illegitimate routes are closed, and reading transcripts so the ones that remain are noticed. See <a href='pages/26-environment-integrity.html'>Environment Integrity</a> and <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "see": [
      "state-based-evaluation",
      "trajectory",
      "reward-hacking",
      "verifier",
      "transcript"
    ]
  },
  "error-analysis": {
    "name": "Error Analysis",
    "short": "The practice of reading real runs one at a time, noting what actually went wrong in each, and grouping the notes into recurring failure categories.",
    "def": "Error analysis means opening the transcripts and reading them, one run at a time, writing down what went wrong, then grouping the notes into categories. It exists because intuition about how a system fails is reliably wrong. For agentic evals, the first and most valuable cut is between failures of the model and failures of the environment, and making that cut is a Linux reading skill. <code>bash: jq: command not found</code> is a missing package. <code>E: Could not get lock /var/lib/dpkg/lock-frontend</code> is another process holding apt. A step that produces nothing for ten minutes is a pager or a prompt waiting for a keypress the agent cannot send. <code>Killed</code> with exit code 137 is usually the memory limit. None of these says anything about capability, and each points at a fix in the image or harness. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "also": "transcript review, failure analysis",
    "see": [
      "failure-mode",
      "transcript",
      "infrastructure-failure",
      "trajectory",
      "exit-status"
    ]
  },
  "failure-mode": {
    "name": "Failure Mode",
    "short": "A recurring, named way that runs go wrong, such as 'hangs on an interactive prompt' or 'assumes bash on Alpine', specific enough to count and to fix.",
    "def": "A failure mode is a pattern of failure with a label. The label matters: until a pattern has a name you cannot count it, rank it against other problems, or tell whether a fix worked. In terminal-based evals a large share turn out to be interactions between agent habits and Linux realities, and they recur across benchmarks: waiting forever on an interactive prompt or pager; using <code>sudo</code> where it is not installed; assuming <code>bash</code> or GNU options on an Alpine image; starting a server in the foreground and blocking on it; running out of disk or memory; fighting a permissions error by making everything world-writable. Naming them lets you separate those that reveal a model weakness from those that reveal an environment bug, and report each honestly. See <a href='pages/27-reading-terminal-transcripts.html'>Reading Terminal Transcripts</a>.",
    "see": [
      "error-analysis",
      "infrastructure-failure",
      "interactive-prompt",
      "transcript",
      "reward-hacking"
    ]
  }
};
