# Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B307 (Use of `eval`) | Security (High) | 47 | Use of `eval()` on `surge_expr` executes arbitrary code, creating a major code injection vulnerability. | Replace dynamic evaluation with explicit, safe arithmetic logic or predefined mathematical operations. |
| B605 / B607 (Command Execution) | Security (High) | 59 | `os.system()` runs shell commands with unsanitized string concatenation, opening the system to shell injection attacks. | Replace the shell invocation with a built-in Python function (e.g., standard `print()` or Python `logging`). |
| B324 (Insecure Hash Function) | Security (Medium) | 51 | `hashlib.md5()` is a cryptographically broken hash function susceptible to collision attacks. | Upgrade to a secure, modern hashing algorithm such as `hashlib.sha256()`. |
| B311 (Standard Pseudo-Random Generator) | Security (Medium) | 55 | `random.randint()` uses a Mersenne Twister PRNG, which is predictable and unsuitable for security pins or tokens. | Use Python's cryptographically secure pseudo-random number generator module, `secrets`. |
| B105 (Hardcoded Password / Key) | Security (Low/Medium) | 70 | Sensitive secret token `gate_barrier_key` is hardcoded in the source file. | Read secrets securely from environment variables (e.g., `os.getenv()`) with a fallback default. |
| W0102 (Dangerous Default Value) | Quality / Bug | 14 | Mutable default argument `entry_logs=[]` persists across separate calls, leaking state between function runs. | Set default to `None` and initialize `entry_logs = []` inside the function body. |
| W0702 / E722 (Bare Except) | Quality / Style | 28 | Bare `except:` catches all exceptions, including `KeyboardInterrupt` and `SystemExit`, masking critical bugs. | Specify exact exceptions, such as `except KeyError:`. |