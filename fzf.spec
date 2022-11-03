%global debug_package %{nil}
%global _commit 04d0b02

# Go 1.18 is required for now
%if 0%{?rhel} >= 10 || 0%{?fedora} >= 36
    %global _need_static_go_bin 0
%else
    %global _need_static_go_bin 1
%endif

Name:           fzf
Version:        0.34.0
Release:        1%{?dist}
Summary:        A command-line fuzzy finder written in Go

License:        MIT
URL:            https://github.com/junegunn/fzf
Source0:        https://github.com/junegunn/fzf/archive/%{version}.tar.gz

BuildRequires:  gcc git make
%if ! %{_need_static_go_bin}
BuildRequires:  golang
%endif

%description
fzf is a general-purpose command-line fuzzy finder.

It's an interactive Unix filter for command-line that can be used with any
list; files, command history, processes, hostnames, bookmarks, git commits,
etc.

%prep
%autosetup

%if %{_need_static_go_bin}
    _GO_VER="$(curl -Lf https://golang.org/VERSION?m=text)"
    %ifarch x86_64
        _ARCH=amd64
    %endif
    %ifarch aarch64
        _ARCH=arm64
    %endif
    if [[ -z "${_ARCH}" ]]; then
        echo "Unsupported architecture!"
        exit 1
    fi
    _GO_DL_NAME="${_GO_VER}.linux-${_ARCH}.tar.gz"
    _GO_DL_URL="https://go.dev/dl/${_GO_DL_NAME}"

    curl -Lfo "${_GO_DL_NAME}" "${_GO_DL_URL}"
    tar -xf "${_GO_DL_NAME}"
    # bins in go/bin
%endif

%build
%if %{_need_static_go_bin}
    _GO_BIN_DIR=$(realpath "go/bin")
    export PATH="${_GO_BIN_DIR}:${PATH}"
%endif

make FZF_VERSION=%{version} FZF_REVISION=%{_commit} all install

%check
%if %{_need_static_go_bin}
    _GO_BIN_DIR=$(realpath "go/bin")
    export PATH="${_GO_BIN_DIR}:${PATH}"
%endif

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
* Wed Sep 28 2022 cyqsimon - 0.34.0-1
- Release 0.34.0

* Mon Aug 29 2022 cyqsimon - 0.33.0-1
- Release 0.33.0
- Re-enable the fixed formatter test

* Tue Aug 09 2022 cyqsimon - 0.32.1-1
- Release 0.32.1

* Fri Aug 05 2022 cyqsimon - 0.32.0-1
- Release 0.32.0
