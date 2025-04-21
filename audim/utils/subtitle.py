import pysrt


class Subtitle:
    """
    Contains utility functions for SRT files
    """

    def replace_speakers(self, srt_file, speakers, in_place=True):
        """
        Replace speaker placeholders with actual names in SRT file

        Example, allows replacing "[Speaker 1]", "[Speaker 2]", etc.
        with actual speaker names such as "[Host]", "[Guest]", etc.

        Args:
            srt_file (str): Path to the SRT file
            speakers (list or dict): Either a list of speaker names in order
                or a dictionary mapping speaker numbers/names to actual names
            in_place (bool): Whether to modify the file in place (default: True)
                If False, returns modified subs without saving

        Returns:
            pysrt.SubRipFile: The modified subtitles object
        """

        # Load the subtitles
        subs = pysrt.open(srt_file)

        # Determine if speakers is a list or dictionary
        speaker_map = {}
        if isinstance(speakers, list):
            # Create mapping from [Speaker N] to [SpeakerName]
            for i, name in enumerate(speakers, 1):
                speaker_map[f"[Speaker {i}]"] = f"[{name.title()}]"
        elif isinstance(speakers, dict):
            # Handle dictionary input
            for key, name in speakers.items():
                # If the key is an integer, convert to [Speaker N] format
                if isinstance(key, int):
                    speaker_map[f"[Speaker {key}]"] = f"[{name.title()}]"
                # If the key already includes 'Speaker', use as is
                elif "Speaker" in str(key):
                    # Ensure proper formatting with brackets
                    formatted_key = (
                        f"[{key}]" if not str(key).startswith("[") else str(key)
                    )
                    formatted_key = (
                        formatted_key
                        if formatted_key.endswith("]")
                        else f"{formatted_key}]"
                    )
                    speaker_map[formatted_key] = f"[{name.title()}]"
                else:
                    # Default case, assume key is the speaker identifier
                    speaker_map[f"[{key}]"] = f"[{name.title()}]"
        else:
            raise ValueError("Speakers must be a list or dictionary")

        # Process each subtitle
        for sub in subs:
            for placeholder, real_name in speaker_map.items():
                # Replace each speaker placeholder with the real name
                sub.text = sub.text.replace(placeholder, real_name)

        # Save changes if requested
        if in_place:
            subs.save(srt_file, encoding="utf-8")

        return subs

    def preview_replacement(self, srt_file, speakers, limit=5, pretty_print=True):
        """
        Preview the speaker replacements without modifying the file

        Args:
            srt_file (str): Path to the SRT file
            speakers (list or dict): Either a list of speaker names in order
                or a dictionary mapping speaker numbers/names to actual names
            limit (int): Maximum number of subtitles to display in preview
            pretty_print (bool): Whether to print a formatted preview to console

        Returns:
            list: List of tuples with (original_text, modified_text)
        """

        # Get modified subs without saving
        modified_subs = self.replace_speakers(srt_file, speakers, in_place=False)
        original_subs = pysrt.open(srt_file)

        # Create preview of changes
        preview = []
        for i, (orig, mod) in enumerate(zip(original_subs, modified_subs)):
            if i >= limit:
                break
            preview.append((orig.text, mod.text))

        if pretty_print:
            print(
                f"\n{'=' * 50}\n"
                f"SPEAKER REPLACEMENT PREVIEW ({limit} entries max)\n"
                f"{'=' * 50}"
            )

            for i, (orig, mod) in enumerate(preview, 1):
                # Highlight the differences
                print(f"\n#{i}: ")
                print(f"  BEFORE: {orig}")
                print(f"  AFTER : {mod}")

                # Only print divider if not the last item
                if i < len(preview):
                    print(f"  {'-' * 48}")

            print(f"\n{'=' * 50}\n")

        return preview
