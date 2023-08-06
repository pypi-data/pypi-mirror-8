
This module contains abstraction to register music file trees, for example
music libraries, playlist directories or loop/sample collections. The module
does not contain useful tools for end users, but is the music library backend
for developing such tools.

All code here is evolution from my previous 'musa' module, which I no more
develop. All functionality of musa may never be moved to soundforest, I
will try to keep this clean, dedicated to the tasks it has planned to do.

Tasks for this module include:
 - Parsing of audio file tags with common API and standardized tag names
   for default tags with all file formats supported

 - Support multiple trees easily, support multiple tree types in addition
   to common 'music file library' tasks (loops,samples,studio recordings)

 - Storing of file trees and tags associated with a source to database:
   source is by default 'filesystem', but same files can be registered
   under custom sources, for example to store data from specific program

 - Storing of abstraction of playlists to database: a playlist has a name
   and contains songs, nothing else, but you can register playlists from
   multiple sources, allowing importer to read data from different programs
   and compare or merge the playlists based on DB info. It's up to the
   module user to import/export this data

 - Tracking of file changes in trees, for 'audio file tree change logs'

 - Configuring various codecs and encoder/decoder commands to database,
   with classes to execute decode/encode operations cleanly from python
   using configured codec commands

