---
index: 1
title: "Easy on the eyes"
excerpt: "Making a portfolio is hard. Making it a beauty to look at is harder. Making it literally easy on the eyes is an art. But art doesn't have to be hard."
publicationDate: "2020-07-05"
slug: easy_on_the_eyes
tags:
- portfolio
- colours
- Solarized
---

# Easy on the eyes

Making a portfolio is hard. Making it a beauty to look at is harder. Making it literally easy on the eyes is an art. But art doesn't have to be hard.
<!--more-->

Good artists borrow, great artists steal. [My portfolio site](https://dhruvkb.github.io/) was my art project, and I wanted everything to be perfect. I wanted people to stay, read, explore and search for Easter eggs laid out across the site. And as a developer, I am no stranger to the strain looking at a screen can cause on the eyes. I have huge glasses from looking at my screen all day and I didn't want people visiting my site to get the same.

An important fact to remember is that designing a website is not easy. There are hundreds of variables to account for such as fonts, copy, design, animations and transitions, just to name a few. That's more than enough on my plate. Add deciding a colour scheme to the mix and you will inevitably end up with a site overrun with poor colour combinations, terrible contrast and poor overall reading experience. Not ideal, not ideal at all.

Anyone who has been in the development business for some time knows the answer to eye strain and screen fatigue. And I've been a patron of this for the longest time, even when I built my [first ever web portfolio in vanilla JavaScript](https://vjs.dhruvkb.now.sh/) way back in 2016. After I remade my portfolio, updated to make use of the latest frontend development technologies, I kept the colour scheme, even going so far as to add in a toggle between the light and dark modes of the same theme.

Let's take some time to meet and learn more about the theme that changed my life. I'm talking, of course, about [Solarized by Ethan Schoonover](https://ethanschoonover.com/solarized). We'll also glance at how I implemented this dual-theme on my portfolio.

Do note that the code given here highlights the most important and interesting parts of the application. There are many more aspects to it that I cannot fully cover here. To understand it fully, please read the [source code](https://github.com/dhruvkb/portfolio) on GitHub. I assure you it is as well-documented as this blog post.

## 1. Solarized

<img
  style="width: 216.5px; height: 217px;"
  alt="00001_solarized.png"
  src="https://raw.githubusercontent.com/dhruvkb/portfolio-blog/master/images/00001_solarized.png">

Solarized is a colour scheme (or theme or palette, whatever you like to call it). That's all it is. It is merely a collection of 8 monotonal colours and 8 accent colours as is customary for terminal-based colour schemes. But there is a something special about these colours that makes saying "These colours work harmoniously together" a massive understatement.

### 1.1. Higher is not always better

White on black and conversely black on white are both too high in terms of the brightness contrast. Increasing the contrast increases readability but eventually it hits a maximum in reading comfort, after which we enter the territory of negative returns. The optimum reading contrast is much less than that the ultimate constrast offered by black/white.

Solarized hits the mark quite perfectly and is not tiresome even when looking at a screen for long durations of time. I use it on my text editor, IDE, browser and terminal. I'm practically looking at Solarized all day, and all night too.

### 1.2. Backed by mathematics

The colours have some unique properties derived from solid principles of colour mathematics. Schoonover designed the 8 monotones with precise CIELAB lightness (L*) and the hues keeping the colour wheel relationships in mind.

As the Solarized website points out the colors monotone colors are more or less consistent in the lightness difference.

| Transition         | L* difference | Transition         |
|--------------------|---------------|--------------------|
| Base 03 to Base 02 | +5            | Base  2 to Base  3 |
| Base 02 to Base 01 | +25           | Base  1 to Base  2 |
| Base 01 to Base 00 | +5            | Base  0 to Base  1 |

The colours get brighter from Base 03 to Base 00 and then further from Base 0 to Base 3. The four middle colours are content and the four extreme colours are backgrounds. Backgrounds are paired with content colours from the other half of the spectrum.

There is a difference of about 45 L* between any of the content tones and the corresponding background tones.

### 1.3. Night and day

We pick four content colors and three background colors from Solarized. These are:
- **Content**
  - **Secondary**: used when some text needs to dodge attention
  - **Normal**: used as the default foreground colour
  - **Highlighted**: used when some text needs to draw attention
  - **Prominent**: used for the most important content on the page
- **Background**
  - **Normal**: used as the default background colour
  - **Highlighted**: used behind highlighted content
  - **Selected**: used as overlay for user-selected content

| Usecase                     | Dark        | Light       |
|-----------------------------|-------------|-------------|
| Content - Secondary         | Base 01     | Base 1      |
| Content _(default)_         | Base 0      | Base 00     |
| Content - Highlighted       | Base 1      | Base 01     |
| Content - Prominent         | Base 2      | Base 02     |
| Background _(default)_      | Base 03     | Base 3      |
| Background - Highlighted    | Base 02     | Base 2      |
| Background - Selected       | 0.1-Base 2  | 0.1-Base 02 |

0.1-Base 2 is `color.adjust(colors.$base-2, $alpha: -0.9)` and 0.1-Base 02 is `color.adjust(colors.$base-02, $alpha: -0.9)`.

## 2. Get your hands dirty

My old portfolio only shipped with the dark version of Solarized. But this time around, the site was much bigger and contained a lot more than just the terminal. There was going to be a blog on the site in addition to 'About' and 'Contact' pages. So I wanted people other than developers to feel at home on the site. I wanted to offer the ability to switch to the light version of the theme should people want it. That's because the light version is much preferable in bright environments and during daytime whereas the dark version shines in dimly lit ones or during nighttime.

Adding this theme switcher would have been way harder before the introduction of CSS custom properties. Now that most popular browsers support CSS custom properties, our work becomes much easier.

We can just define all the colors as Sass variables to enable using them across the site. I like to put all my constants inside separate files under a `tokens/` folder. That way changing them is easy because there's a central location from where all compone nts are deriving their properties.

```scss
/* styles/tokens/_colors.scss */
// Greyscale tones

$base-03:        #002b36; // L* 15
$base-02:        #073642; // L* 20
$base-01:        #586e75; // L* 45
$base-00:        #657b83; // L* 50
$base-0:         #839496; // L* 60
$base-1:         #93a1a1; // L* 65
$base-2:         #eee8d5; // L* 92
$base-3:         #fdf6e3; // L* 97

// Accent colors

$accent-yellow:  #b58900; // Split comp
$accent-orange:  #cb4b16; // Complement
$accent-red:     #dc322f; // Triad
$accent-magenta: #d33682; // Tetrad
$accent-violet:  #6c71c4; // Analogous
$accent-blue:    #268bd2; // Monotone
$accent-cyan:    #2aa198; // Analogous
$accent-green:   #859900; // Tetrad

$accents: (
  'yellow':      $accent-yellow,
  'orange':      $accent-orange,
  'red':         $accent-red,
  'magenta':     $accent-magenta,
  'violet':      $accent-violet,
  'blue':        $accent-blue,
  'cyan':        $accent-cyan,
  'green':       $accent-green
);
```

We then use this tokens to define two versions of the theme under the appropriately named classes, `.dark-themed` and `light-themed`, that can be applied to the root HTML element. The best part is that these CSS variables are inherited by every element in the entire application.

```scss
/* styles/base/theme.scss */
@use '~@/styles/tokens/colors';

@mixin dark-theme {
  #{--content-secondary}:      colors.$base-01;
  #{--content}:                colors.$base-0;
  #{--content-highlighted}:    colors.$base-1;
  #{--content-prominent}:      colors.$base-2;

  #{--background}:             colors.$base-03;
  #{--background-highlighted}: colors.$base-02;
  #{--background-selected}:    color.adjust(colors.$base-2, $alpha: -0.9);
}

@mixin light-theme {
  #{--content-secondary}:      colors.$base-1;
  #{--content}:                colors.$base-00;
  #{--content-highlighted}:    colors.$base-01;
  #{--content-prominent}:      colors.$base-02;

  #{--background}:             colors.$base-3;
  #{--background-highlighted}: colors.$base-2;
  #{--background-selected}:    color.adjust(colors.$base-02, $alpha: -0.9);
}

@mixin theme {
  @media (prefers-color-scheme: dark) {
    @include dark-theme;
  }
  @media not all and (prefers-color-scheme: dark) {
    @include light-theme;
  }

  &[theme="dark"] {
    @include dark-theme;
  }

  &[theme="light"] {
    @include light-theme;
  }
}

:root {
  @include theme;
}

body {
  color: var(--content);
  background-color: var(--background);
}
```

As a fan of symmetry, I appreciate how you can toggle the leading zero to change from the dark to the light version of Solarized and vice versa. Switching colours in Solarized is also made easier by the accent colours being the same for both versions of the theme. This directly cuts down on the number of elements that will change colours in the theme change transition.

First and foremost, we want the change to be smooth instead of sudden and jarring. A brute-force solution to this is to apply a transition on every element in the DOM tree. We'll just go with it for now.

```scss
/* styles/base/theme.scss */
* {
  transition-property: color, background-color;
  transition-duration: 0.5s;
}
```

Next we need a way for the user to change the theme and for the site to memorise the last used theme and use that by default on the subsequent visits. With my framework of choice being Vue.js, I was able to accomplish this fairly easily with the `Themer` component.

See the [code for the `Themer` component](https://github.com/dhruvkb/portfolio/blob/master/src/app/components/themer/Themer.vue).

Let me break that down for you. The `Themer` component contains two data variables, `themes`, listing all possible themes supported by the app, and `theme`, the currently active one, set to `null` at mount time, but resolving to one of the possible themes immediately after.

```js
// components/app/themer/Themer.vue script
export default {
  // ...
  data () {
    return {
      themes: {
        system: {
          themeColor: null // automatically maps to light or dark
        },
        light: {
          themeColor: colors.colorBackgroundBase2
        },
        dark: {
          themeColor: colors.colorBackgroundBase02
        }
      },
      theme: null,
      default: 'system'
    }
  }
}
```

We start with a person opening my portfolio on their device. By place the themer component in the navbar, we ensure it is loaded on every page and as soon as it is created it invokes the `created()` lifecycle function.

```js
// components/app/themer/Themer.vue script
export default {
  // ...
  created () {
    if (localStorage.theme) {
      // Switch to last used theme
      this.theme = localStorage.theme
    } else {
      this.theme = 'dark'
    }
  }
}
```

In the function we check if the local storage contains the key `'theme'`. If it does, that means the user has visited the site before and so we switch the user over to the last by setting the data variable `theme` to the value retrived from local storage. If it doesn't, we switch to the dark theme, which is the default as it is my favourite. Either way, the value of the variable `theme` changes and our watcher is triggered with the values of the old and new themes.

```js
// components/app/themer/Themer.vue script
export default {
  // ...
  watch: {
    theme (to, from) {
      if (to !== from) { // Breaks recursion
        document.documentElement.setAttribute('theme', this.theme)

        // Set the new theme color
        this.themeColorElement.content = this.themeColor

        // Persist theme to local storage
        localStorage.theme = to
      }
    }
  }
}
```

Whenever the value of `to` from is different from that of `from`, we know a theme change has occurred so we change the attribute on the HTML element and subsequently write the new value of the theme to the local storage to preserve it for the future. After all, good software cares for and remembers the preferences of their users.

Finally we need to add a button that allows the user to change the theme at will. The template for that will look a little something like this.

```html
<!-- components/app/themer/Themer.vue template -->
<button @click="switchTheme('system')">System theme</button>
<button @click="switchTheme('light')">Light theme</button>
<button @click="switchTheme('dark')">Dark theme</button>
```

We haven't defined the `switchTheme()` method yet so the next step would be doing exactly that.

```js
// components/app/themer/Themer.vue script
export default {
  // ...
  methods: {
    switchTheme (theme) {
      this.theme = theme
    }
  }
}
```

That's all there is to it. Now you know the story of why, and how, my new portfolio contains functionality to choose from two different themes, both of which are comfortable for the eyes while remaining easily associated with activities like reading text and writing code.

## 3. Portfolio series

This post is part one of my series covering my [new portfolio website](https://dhruvkb.github.io/).

1. Easy on the eyes
2. [Blogging on a static site](https://dhruvkb.github.io/#/blog/post/blogging_on_a_static_site)
3. [Push and it's live](https://dhruvkb.github.io/#/blog/post/push_and_its_live)
4. [Back to the future](https://dhruvkb.github.io/#/blog/post/back_to_the_future)

For the tech-savvy, the [open-source, well-documented code](https://github.com/dhruvkb/portfolio) powering my portfolio is available on GitHub. I'm sure that you can either learn something from it or teach me something about it so please reach out!

Hope you enjoyed reading this. Till next time!

~ @dhruvkb
