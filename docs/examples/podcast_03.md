# Advanced Video Effects with Progressive Disclosure of Complexity

> - **Author**: [@mratanusarkar](https://github.com/mratanusarkar)
> - **Created**: April 16, 2025
> - **Last Updated**: April 17, 2025
> - **Compatible with**: Audim v0.0.1

This example explores Audim's implementation of the "progressive disclosure of complexity" design principle through the `effects` module in the `sub2pod` package. We'll demonstrate how Audim provides a smooth learning curve for users of all experience levels.

## What is Progressive Disclosure of Complexity?

Progressive disclosure of complexity is a design principle that gradually reveals advanced functionality as users become more experienced with a system. This concept originated in UI design but has been adapted for API design in software libraries.

Specially in module or library design, this principle is realized by creating higher level APIs and lower level APIs. While the lower level APIs are granular, fundamental, small and rigid catering to specific functionalities of the module or library. The higher level APIs are complex and formed by combining the lower level APIs catering to specific end user requirements and use cases.

This results in end users using the higher level APIs with ease, getting out of the box experience, while also being able to dig deeper into the lower level APIs for specific customizations when needed.

As described by design experts:

> "Progressive disclosure is an interaction design technique that sequences information and actions across several screens in order to reduce feelings of overwhelm for the user." - [Interaction Design Foundation](https://www.interaction-design.org/literature/book/the-glossary-of-human-computer-interaction/progressive-disclosure)

This approach is used by many popular libraries like [Keras](https://keras.io/getting_started/about/#keras-follows-the-principle-of-progressive-disclosure-of-complexity), [Hugging Face Transformers](https://huggingface.co/blog/transformers-design-philosophy), [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/en/conceptual/philosophy) and many more allowing users to:

- Start simple with sensible defaults
- Incrementally discover more advanced features
- Access the full power of the library when needed

## How Audim's `sub2pod` submodule Implements Progressive Disclosure

Audim's `sub2pod` submodule implements progressive disclosure of complexity as follows:

- The end user is expected to use the `VideoGenerator` object in the `core` module to render and generate the final video.
- The end user is expected to use the highest level API: `PodcastLayout` object in the `layouts` module.
- The `PodcastLayout` object internally uses the `elements` and `effects` modules.
- An implementation of podcast is given out of the box with the `PodcastLayout` object.
- If the end user wishes to create their own custom layout, they can do so by using the `BaseLayout` class.
- Similarly, if users need further customizations of the fundamental elements and effects, they can dig deeper into the `elements` and `effects` modules.
- Each of these modules comes with their own args and kwargs to allow for further customization and fine-tuning of the elements and effects.
- Power users can also implement their own custom elements and effects by subclassing the `BaseElement` and `BaseEffect` classes.
- So, by providing API abstractions from higher levels to the lower levels, Audim's `sub2pod` submodule allows users to:
  - Start using and generation podcast videos out of the box with sensible defaults
  - Incrementally discover more advanced features and customizations when needed
  - Access the full power of the library when needed with fine-tuned control over the layouts, elements and effects
  - Power users can also implement their own custom layouts, elements and effects by subclassing the `BaseLayout`, `BaseElement` and `BaseEffect` classes.

## Why this is powerful?


### 1. Progressive Disclosure of Complexity

This approach creates a natural hierarchy of complexity:
- **Simple level**: Users choose a pre-configured layout with default effects
- **Intermediate level**: Users customize effects for elements on existing layouts
- **Advanced level**: Users create custom layouts with custom elements and effects

This matches how video editors typically work - first selecting templates, then adjusting effects, and finally creating custom compositions when needed.

### 2. End User Experience

For video creators and editors, this model is intuitive because:
- It follows familiar mental models from tools like OBS, Premiere Pro, and After Effects
- Effects are naturally tied to how content appears (the layout)
- The separation keeps the API clean while maintaining flexibility
- Users can think in terms of "scenes" (layouts) that have both positioning and visual effects


## How the new `effects` module Implements Progressive Disclosure

Audim's `effects` module provides transition and highlight effects for videos with three distinct levels of complexity:

1. **Level 1: Default Usage** - No configuration needed
2. **Level 2: Simple Customization** - Basic string-based configuration
3. **Level 3: Advanced Customization** - Detailed parameter configuration

This approach allows beginners to get started quickly while giving advanced users the power and flexibility they need.

## Example: Three Levels of Complexity

Let's explore how you can use Audim's effects at different complexity levels:

### Level 1: Default Usage (No Configuration)

The simplest way to use Audim is with default settings. The `PodcastLayout` automatically includes a default fade transition:

```python
from audim.sub2pod.layouts.podcast import PodcastLayout
from audim.sub2pod.core import VideoGenerator

# Create a podcast layout with default fade transition
layout = PodcastLayout(
    video_width=1920, 
    video_height=1080,
    show_speaker_names=True
)

# Add speakers
layout.add_speaker("Host", "input/host.png")
layout.add_speaker("Guest", "input/guest.png")

# Create generator with this layout
generator = VideoGenerator(layout)

# The layout will automatically use the default fade transition
# No explicit configuration needed!
```

At this level, users don't need to know anything about effects - they just work.

### Level 2: Simple Customization

As users become more comfortable, they can easily customize effects by simply specifying the effect type:

```python
# Create podcast layout
layout = PodcastLayout(
    video_width=1920,
    video_height=1080,
    show_speaker_names=True
)

# Simple customization - just specify effect type
layout.set_transition_effect("slide")  # Use slide transition instead of fade
layout.set_highlight_effect("glow")    # Add glow effect to emphasized text

# Add speakers and generate video as before
```

This level introduces a clean, string-based API that's easy to understand and use.

### Level 3: Advanced Customization

Power users can access detailed customization options when they need fine-grained control:

```python
# Create podcast layout
layout = PodcastLayout(
    video_width=1920,
    video_height=1080,
    show_speaker_names=True
)

# Advanced customization with detailed parameters
layout.set_transition_effect(
    "slide", 
    frames=25,                  # Longer transition (default: 15 frames)
    direction="left"            # Slide in from left
)

layout.set_highlight_effect(
    "pulse",
    color=(255, 215, 0, 100),   # Custom gold color, semi-transparent
    min_size=0.9,               # Subtle pulse (90% to 110% size)
    max_size=1.1,
    blur_radius=8               # More blur for softer effect
)

# Add speakers and generate video as before
```

At this level, users have complete control over every aspect of the effects.

## Full Implementation Example

Here's how you might use Audim's `sub2pod` submodule in a complete project:

```python
from datetime import datetime
from audim.sub2pod.layouts.podcast import PodcastLayout
from audim.sub2pod.core import VideoGenerator

# Create a podcast layout
print("Creating layout...")
layout = PodcastLayout(
    video_width=1920,
    video_height=1080,
    show_speaker_names=True
)

# Set custom effects for the layout
layout.set_transition_effect("fade", frames=20)
layout.set_highlight_effect("none")

# Add speakers
print("Adding speakers...")
layout.add_speaker("Grant Sanderson", "input/grant.png")
layout.add_speaker("Sal Khan", "input/sal.png")

# Generate video
print("Generating video...")
generator = VideoGenerator(layout, fps=30)
generator.generate_from_srt(
    srt_path="input/podcast.srt",
    audio_path="input/podcast.mp3",
    logo_path="input/logo.png",
    title="3b1b Podcast: Sal Khan: Beyond Khan Academy",
    cpu_core_utilization="max"
)

# Export the final video
print("Exporting video...")
datetime = datetime.now().strftime("%Y%m%d%H%M%S")
generator.export_video(f"output/podcast_underline_{datetime}.mp4")
```

## Available Effects

### Transition Effects

Transitions control how each frame fades in or slides into view:

| Effect Type | Description | Parameters |
|-------------|-------------|------------|
| `"none"` | No transition (default) | None |
| `"fade"` | Smooth fade-in transition | `frames`: Duration of fade |
| `"slide"` | Slide-in animation | `frames`: Duration of slide, `direction`: "left", "right", "up", or "down" |

### Highlight Effects

Highlights emphasize the active speaker's text:

| Effect Type | Description | Parameters |
|-------------|-------------|------------|
| `"none"` | No highlight | None |
| `"pulse"` | Pulsing animation | `color`, `min_size`, `max_size`, `blur_radius` |
| `"glow"` | Glowing background | `color`, `blur_radius` |
| `"underline"` | Simple underline | `color`, `thickness` |
| `"box"` | Box around text | `color`, `padding`, `thickness` |

## Benefits of Progressive Disclosure

This design pattern offers several advantages:

1. **Reduced Learning Curve**: New users can be productive immediately without being overwhelmed
2. **Smooth Progression**: Users can gradually discover more advanced features as they need them
3. **Documentation Organization**: Documentation can target different user groups based on expertise
4. **API Cleanliness**: The API remains clean and intuitive at all levels
5. **Flexibility**: Advanced users can access powerful features without sacrificing simplicity for beginners

## Real-World Impact

The progressive disclosure pattern in Audim helps different types of users:

- **Content Creators**: Can quickly generate basic podcast videos without technical knowledge
- **Video Editors**: Can customize effects to match their brand and style
- **Developers**: Can achieve precise control and integrate Audim into larger workflows

## Troubleshooting

If you encounter issues with effects:

- Verify you're using Audim v0.0.1 or later
- Check that effect names are spelled correctly (e.g., "fade" not "fading")
- For slide transitions with text, ensure your text color includes an opacity value
- When using highlight effects, ensure the subtitle area is properly defined

## See Also

- [Basic Podcast Example](/examples/podcast_01)
- [Professional Podcast Example](/examples/podcast_02)
- [API Documentation for Transitions](/audim/sub2pod/effects/transitions)
- [API Documentation for Highlights](/audim/sub2pod/effects/highlights)
