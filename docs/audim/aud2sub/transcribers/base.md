# Base Transcriber

The base transcriber is the base class for all transcriber classes.
It defines the interface for all transcriber classes.

It must be overriden to create various transcriber classes with various **ASR models**,
**diarization models**, **alignment models**, **formatters** and their implementations.

It determines the subtitle generation pipeline and format of the subtitle generation.

Below is the API documentation for the base transcriber:

::: audim.aud2sub.transcribers.base
