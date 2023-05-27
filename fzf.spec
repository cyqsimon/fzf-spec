%global debug_package %{nil}
%global _commit 6eb1874

Name:           fzf
Version:        0.41.1
Release:        1%{?dist}
Summary:        A command-line fuzzy finder written in Go

License:        MIT
URL:            https://github.com/junegunn/fzf
Source0:        https://github.com/junegunn/fzf/archive/%{version}.tar.gz

BuildRequires:  git golang make

%description
fzf is a general-purpose command-line fuzzy finder.

It's an interactive Unix filter for command-line that can be used with any
list; files, command history, processes, hostnames, bookmarks, git commits,
etc.

%prep
%autosetup

%build
make FZF_VERSION=%{version} FZF_REVISION=%{_commit} all install

%check
make FZF_VERSION=%{version} FZF_REVISION=%{_commit} test

%install
# bin
mkdir -p %{buildroot}%{_bindir}
install -Dpm 755 -t %{buildroot}%{_bindir} bin/%{name}{,-tmux}

# manpage
mkdir -p %{buildroot}%{_mandir}/man1
install -Dpm 644 -t %{buildroot}%{_mandir}/man1 man/man1/%{name}{,-tmux}.1

# completions & keybindings
## not enabled by default for bash & zsh
mkdir -p %{buildroot}%{_datadir}/%{name}
install -Dpm 644 -t %{buildroot}%{_datadir}/%{name} shell/{completion,key-bindings}.{bash,zsh}

## enabled by default for fish (actually I'm not sure if it does or why)
## See https://github.com/archlinux/svntogit-community/blob/packages/fzf/trunk/PKGBUILD
install -Dpm 644 shell/key-bindings.fish \
    %{buildroot}%{_datadir}/fish/vendor_functions.d/%{name}_key_bindings.fish

# vim plugin
mkdir -p %{buildroot}%{_datadir}/vim/vimfiles/{doc,plugin}
install -Dpm 644 -t %{buildroot}%{_datadir}/vim/vimfiles/doc doc/%{name}.txt
install -Dpm 644 -t %{buildroot}%{_datadir}/vim/vimfiles/plugin plugin/%{name}.vim

%files
%license LICENSE
%doc ADVANCED.md CHANGELOG.md README.md README-VIM.md doc/%{name}.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-tmux
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-tmux.1*
%{_datadir}/%{name}/*
%{_datadir}/fish/vendor_functions.d/%{name}_key_bindings.fish
%{_datadir}/vim/vimfiles/doc/%{name}.txt
%{_datadir}/vim/vimfiles/plugin/%{name}.vim

%changelog
* Sat May 27 2023 cyqsimon - 0.41.1-1
- Release 0.41.1

* Fri May 26 2023 cyqsimon - 0.41.0-1
- Release 0.41.0

* Sun Apr 30 2023 tessus - 0.40.0-1
- Release 0.40.0

* Sun Apr 02 2023 tessus - 0.39.0-1
- Release 0.39.0

* Wed Feb 15 2023 tessus - 0.38.0-1
- Release 0.38.0

* Tue Jan 24 2023 tessus - 0.37.0-1
- Release 0.37.0

* Tue Jan 17 2023 cyqsimon - 0.36.0-1
- Release 0.36.0

* Sat Nov 19 2022 cyqsimon - 0.35.1-1
- Release 0.35.1
- Set correct commit hash

* Sat Nov 12 2022 cyqsimon - 0.35.0-1
- Release 0.35.0

* Wed Sep 28 2022 cyqsimon - 0.34.0-1
- Release 0.34.0

* Mon Aug 29 2022 cyqsimon - 0.33.0-1
- Release 0.33.0
- Re-enable the fixed formatter test

* Tue Aug 09 2022 cyqsimon - 0.32.1-1
- Release 0.32.1

* Fri Aug 05 2022 cyqsimon - 0.32.0-1
- Release 0.32.0
