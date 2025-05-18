# Dev Blog

This is a blog space documenting the development of the Audim project.

It contains details of version wise updates and progression of the project in a blog format.
You can treat it as a changelog for the project, or a brain dump and thought process dump during the development of the project.

## Blog Contents

Each blog post might include (and not limited to) the following:

- changes made in each version
- rationale behind the changes
- design decisions
- features added
- end user usage and code snippets

| Blog Post | Date | Description |
|-----------|------|-------------|
| [v0.0.1](./v0.0.1.md)  | Mar 05, 2025 | generate basic video from SRT files |
| [v0.0.2](./v0.0.2.md)  | Mar 13, 2025 | making professional podcast video from SRT files |
| [v0.0.3](./v0.0.3.md)  | Apr 16, 2025 | cleaner design with progressive disclosure of complexity |
| v0.0.4                 | NA           | no blog post |
| [v0.0.5](./v0.0.5.md)  | May 15, 2025 | SRT transcription from audio + playback utility |
| [v0.0.6](./v0.0.6.md)  | May 18, 2025 | Audio extraction from video files |

## Changelog

Since we are documenting the development of the project, why not have a changelog and PR trackers for the project?

| Version | Date | Modules Affected | Feature Changes | PR Links |
|---------|------|------------------|-----------------|----------|
| v0.0.1  | Mar 05, 2025 | `sub2pod`            | subtitle text to podcast video                   | [#3](https://github.com/mratanusarkar/audim/pull/3) |
| v0.0.2  | Mar 13, 2025 | `sub2pod`            | optimize & parallize `sub2pod`                   | [#5](https://github.com/mratanusarkar/audim/pull/5) |
| v0.0.3  | Apr 17, 2025 | `sub2pod`            | `effects` submodule + design changes             | [#11](https://github.com/mratanusarkar/audim/pull/11) |
| v0.0.4  | Apr 22, 2025 | `aud2sub`, `sub2pod` | audio to srt + ts normalization + pos offset     | [#15](https://github.com/mratanusarkar/audim/pull/15), [#14](https://github.com/mratanusarkar/audim/pull/14), [#13](https://github.com/mratanusarkar/audim/pull/13) |
| v0.0.5  | Apr 22, 2025 | `util`               | playback audio with subs + replace speaker names | [#17](https://github.com/mratanusarkar/audim/pull/17) |
| v0.0.6  | May 15, 2025 | `util`               | extract audio from video                         | [#24](https://github.com/mratanusarkar/audim/pull/24) |
