#!/bin/bash

# Spaces will be replaced with '-'
TITLE=`read -ra words <<< $1 && echo "${words[@]^}"`
NAME="${TITLE// /-}"


DATE=`date "+%Y-%m-%d"`
POSTNAME=$DATE-$NAME.md


cat <<EOT >> _posts/$POSTNAME
---
title: $TITLE
image: /images/default-cover-image.png
layout: post
description: ToDo
date:   $DATE
tags:   [deep-learning, machine-learning, neural-network]
---

# Contents

1. TOC
{:toc}

EOT

echo created file $POSTNAME in _posts/
