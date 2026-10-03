# Cart total disappears after removal

Synthetic sample, no customer data. Add Notebook ($12) and Ceramic mug ($18). Remove Notebook. Expected: Ceramic mug remains and total is $18.00. Actual in the preserved buggy revision: Ceramic mug remains but total is $0.00.

The bug is a stale derived value returned by `removeItem`. Fixed version derives the total from remaining items. No checkout, payment or backend is involved.
