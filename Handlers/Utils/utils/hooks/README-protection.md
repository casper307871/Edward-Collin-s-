Edward — Archive & Clone Protection

Goals:
- Produce an immutable offline archive (git bundle + signed tarball)
- Enforce repository-level controls: signed commits, access control, and server-side hooks
- Provide runtime license verification for distributed clones

Steps to adopt:
1. Use create_antique_copy.sh to produce offline archival copies. Store offline and on secure backups.
2. Host repo on a private Git server with per-key authorized access.
3. Require developers to sign commits (GPG). Enforce via pre-receive hook.
4. Implement the license server and issue short-lived, machine-bound licenses for production clones.
5. Distribute code via a controlled process (protected_clone.sh) that validates tokens against the license server.
6. Use launcher.py to enforce runtime license checks on distributed instances.

Limitations:
- Nothing is absolutely copy-proof; determined attackers with code and runtime access can bypass protections.
- Security improves by: limiting access, performing code obfuscation, moving critical logic onto server-side services (so clones only get a thin client), and using hardware-backed keys (HSM/TPM).

Contact admin for setup details.
