import subprocess
import sys
import os


class KeyNotFound(Exception):
    pass


class FingerprintDoesNotParse(Exception):
    pass


class KeyLibrary:
    def __init__(self, path, verbose):
        self._path = path
        self._verbose = verbose
        self.keys_by_fingerprint = {}

    def _generate_public_key(self, fname):
        pkey_fname = fname + '.pub'
        if os.access(pkey_fname, os.R_OK):
            return
        print("public key does not exist for private key '%s'" % fname, file=sys.stderr)
        print("attemping to generate; you may be prompted for a passphrase.", file=sys.stderr)
        try:
            public_key = subprocess.check_output(['ssh-keygen', '-y', '-f', fname])
        except subprocess.CalledProcessError:
            return
        with open(pkey_fname, 'wb') as fd:
            fd.write(public_key)
        print("Generated public key successfully.", file=sys.stderr)
        return True

    @classmethod
    def _fingerprint_from_keyinfo(cls, output):
        parts = [s for s in (t.strip() for t in output.split(' ')) if s]
        if len(parts) != 4:
            raise FingerprintDoesNotParse()
            raise
        return parts[1]

    def _scan_key(self, fname, recurse=False):
        try:
            output = subprocess.check_output(['ssh-keygen', '-l', '-f', fname]).decode('utf8')
            try:
                return KeyLibrary._fingerprint_from_keyinfo(output)
            except FingerprintDoesNotParse:
                print("warning: public key fingerprint couldn't be parsed: '%s'" % fname, file=sys.stderr)
                print(output, file=sys.stderr)
        except subprocess.CalledProcessError:
            if not recurse and self._generate_public_key(fname):
                return self._scan_key(fname, recurse=True)

    def scan(self, add_keys=False):
        skip = set(('config', 'known_hosts', 'authorized_keys'))
        for dirpath, dirnames, fnames in os.walk(self._path):
            for name, path in ((t, os.path.join(dirpath, t)) for t in fnames):
                if name.startswith('.'):
                    continue
                if name.endswith('.pub'):
                    continue
                if name in skip:
                    continue
                fingerprint = self._scan_key(path)
                if fingerprint is not None:
                    if self._verbose:
                        print("scanned key '%s' fingerprint '%s'" % (os.path.relpath(path, self._path), fingerprint))
                    if add_keys:
                        subprocess.call(['ssh-add', path])
                    self.keys_by_fingerprint[fingerprint] = path

    def lookup(self, fingerprint):
        try:
            return self.keys_by_fingerprint[fingerprint]
        except KeyError:
            raise KeyNotFound()
