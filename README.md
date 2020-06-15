<!-- PROJECT LOGO -->
<p align="center">
  <h3 align="center">Image Smoothing via L0 Gradient Minimization</h3>

  <p align="center">
    <br />
    <a
    href="https://nthere.dev/2020/06/15/Image-Smoothing-using-L0-Gradient-Minimization/">Blog
    Post</a>
    |
    <a href="https://github.com/nrupatunga/L0-Smoothing/issues">Report Bug</a>
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
	- [Code Setup](#code-setup)

<!--ABOUT THE PROJECT-->
## About the Project

This repository is the Python implementation of the paper:
[Image Smoothing via L0 Gradient Minimization](http://www.cse.cuhk.edu.hk/~leojia/papers/L0smooth_Siggraph_Asia2011.pdf)

|Flower     | Rock
|-----------|-------------|
|![](https://github.com/nrupatunga/L0-Smoothing/blob/master/src/output/flower.png) |![](https://github.com/nrupatunga/L0-Smoothing/blob/master/src/output/rock2.png) |

<!--GETTING STARTED-->
## Getting Started

#### Code Setup
```
# Clone the repository
$ git clone https://github.com/nrupatunga/L0-Smoothing.git

# install all the required repositories
$ cd L0-Smoothing
$ pip install -r requirements.txt

# Run
$ cd src

# To run on single image, modify image path in L0_Smoothing.py
$ python L0_Smoothing.py

# To run on multiple image, modify root directory  in L0_Smoothing.py
$ python run_batch.py

```
