%global debug_package %{nil}

Name:           fzf
Version:        0.56.0
Release:        1%{?dist}
Summary:        A command-line fuzzy finder written in Go

License:        MIT
URL:            https://github.com/junegunn/fzf
Source0:        https://github.com/junegunn/fzf/archive/v%{version}.tar.gz

BuildRequires:  git golang jq make

%description
fzf is a general-purpose command-line fuzzy finder.

It's an interactive Unix filter for command-line that can be used with any
list; files, command history, processes, hostnames, bookmarks, git commits,
etc.

%prep
%autosetup

# Fetch commit SHA
set -o pipefail
API_BASE_URL="https://api.github.com/repos/junegunn/fzf/git"
TAG_INFO="$(curl -Ssf "${API_BASE_URL}/ref/tags/v%{version}")"
if jq -e '.object.type == "tag"' <<< "$TAG_INFO"; then
    # annotated tag
    TAG_SHA=$(curl -Ssf "${API_BASE_URL}/ref/tags/v%{version}" | jq -re '.object.sha')
    COMMIT_SHA=$(curl -Ssf "${API_BASE_URL}/tags/${TAG_SHA}" | jq -re '.object.sha')
else
    # lightweight tag
    COMMIT_SHA=$(jq -re '.object.sha' <<< "$TAG_INFO")
fi
COMMIT_SHA_SHORT=$(head -c 7 <<< ${COMMIT_SHA})
echo "${COMMIT_SHA_SHORT}" > REV

%build
make GOOS=linux FZF_VERSION=%{version} FZF_REVISION=$(cat REV) all install

%check
make GOOS=linux FZF_VERSION=%{version} FZF_REVISION=$(cat REV) test

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
* Sun Oct 27 2024 cyqsimon - 0.56.0-1
- Release 0.56.0

* Thu Aug 29 2024 cyqsimon - 0.55.0-1
- Release 0.55.0

* Thu Aug 01 2024 cyqsimon - 0.54.3-1
- Release 0.54.3

* Sat Jul 27 2024 cyqsimon - 0.54.2-1
- Release 0.54.2

* Fri Jul 19 2024 cyqsimon - 0.54.1-1
- Release 0.54.1

* Tue Jul 09 2024 cyqsimon - 0.54.0-3
- Fix API URL

* Tue Jul 09 2024 cyqsimon - 0.54.0-2
- Fix source URL

* Tue Jul 09 2024 cyqsimon - 0.54.0-1
- Release 0.54.0

* Fri Jun 07 2024 cyqsimon - 0.53.0-1
- Release 0.53.0

* Tue May 14 2024 cyqsimon - 0.52.1-1
- Release 0.52.1

* Wed May 08 2024 cyqsimon - 0.52.0-1
- Release 0.52.0

* Thu May 02 2024 cyqsimon - 0.51.0-2
- Explicitly set `GOOS=linux`

* Thu May 02 2024 cyqsimon - 0.51.0-1
- Release 0.51.0

* Mon Apr 15 2024 cyqsimon - 0.50.0-1
- Release 0.50.0

* Fri Apr 05 2024 cyqsimon - 0.49.0-1
- Release 0.49.0

* Sun Mar 17 2024 cyqsimon - 0.48.1-1
- Release 0.48.1

* Thu Mar 14 2024 cyqsimon - 0.48.0-1
- Release 0.48.0

* Sun Mar 10 2024 cyqsimon - 0.47.0-1
- Release 0.47.0

* Thu Feb 01 2024 cyqsimon - 0.46.1-1
- Release 0.46.1

* Wed Jan 24 2024 cyqsimon - 0.46.0-1
- Release 0.46.0

* Mon Jan 01 2024 cyqsimon - 0.45.0-1
- Release 0.45.0

* Sun Nov 19 2023 cyqsimon - 0.44.1-3
- Fix commit SHA fetch

* Sat Nov 18 2023 cyqsimon - 0.44.1-2
- Automatically obtain commit SHA

* Fri Nov 17 2023 cyqsimon - 0.44.1-1
- Release 0.44.1

* Mon Nov 13 2023 cyqsimon - 0.44.0-1
- Release 0.44.0

* Sun Oct 15 2023 cyqsimon - 0.43.0-1
- Release 0.43.0

* Thu Jun 15 2023 cyqsimon - 0.42.0-1
- Release 0.42.0
- Re-enable tests

* Sat May 27 2023 cyqsimon - 0.41.1-1
- Release 0.41.1
- Temporarily disable tests

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
