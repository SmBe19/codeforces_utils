# codeforces_utils
Utilities for Codeforces

## Login to Codeforces
To use this utility to its fullest, you should log into Codeforces and store the cookie in a file called `~/.codeforces_cookie`. You only need the cookie called `JSESSIONID`. You can change the path of the cookie file by setting the environment variable `CF_COOKIE`.

## Fast Solve
Install [Slide](https://github.com/SmBe19/slide). Then, run `./fast_solve.py <url>` with the url of the problem you want to solve. This will create a new file, insert the testdata into it and paste the problem description as a comment in the file. Slide will watch the file, recompiling it and checking the testdata automatically. Hit enter to submit the file.

You can also run `./install/install_fast_solve.py` to install the `cf` utility. Note that this will link to the current directory, so you should not move the checkout of this repository afterwards.
