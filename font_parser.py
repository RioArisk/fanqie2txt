from fontTools.ttLib import TTFont, woff2
import json

# Decompress WOFF2 to TTF
with open('font.woff2', 'rb') as f_in, open('font.ttf', 'wb') as f_out:
    woff2.decompress(f_in, f_out)

# Load the TTF font
font = TTFont('font.ttf')

# Get the character mapping
cmap = font.getBestCmap()

# The font obfuscation typically maps real characters to the Private Use Area (PUA).
# The PUA characters are then mapped to the correct glyphs.
# We need to find the inverse mapping: from the PUA character to the real character.
# The real characters are usually stored in the '.notdef' glyph's name or in another custom table.
# Let's inspect the glyph names to see if we can find any clues.

glyph_names = font.getGlyphOrder()

# Let's assume the mapping is based on the glyph names.
# For example, a glyph for "A" might be named "uni41" or "A".
# The obfuscated characters will have some other names.
# Let's try to build a mapping based on a common pattern.
# The pattern seems to be: obfuscated char is a PUA character, and the glyph name is like "uniXXXX" where XXXX is the hex code of the real character.
# For example, if a glyph is named "uni4E00", the real character is '\u4e00'.

char_map = {}
for code, name in cmap.items():
    if name.startswith('uni'):
        try:
            real_char_code = int(name[3:], 16)
            real_char = chr(real_char_code)
            obfuscated_char = chr(code)
            char_map[obfuscated_char] = real_char
        except ValueError:
            pass

# Let's try another approach. The mapping could be simpler.
# What if the glyphs are in the same order as the real characters, but the character codes are different?
# For example, the first glyph might be for 'A', the second for 'B', and so on.
# The obfuscated characters are just a sequence of PUA characters.
# Let's try to find the real characters from another source.
# The problem is, where are the real characters stored?

# A common technique is to have a base font with the correct mappings, and then create a new font with the scrambled cmap.
# The glyphs themselves might contain the information.

# Let's try to get the content from the HTML and see if we can find a pattern.
# I'll need to read the HTML file I downloaded earlier.
# I can't do that from this script.

# Let's just print the cmap for now and see what it looks like.
# I'll save it to a file so I can inspect it.
with open('cmap.json', 'w', encoding='utf-8') as f:
    json.dump({k: v for k, v in cmap.items()}, f, ensure_ascii=False, indent=2)

# I also need to get the novel content. I'll do that in a separate step.
# For now, let's focus on the font.

# The user mentioned that the numbers are not obfuscated. This is a very important clue.
# Let's check the cmap for numbers.
# The unicode for '0' is 48.
# Let's see what glyph is mapped to character code 48.
if 48 in cmap:
    print(f"Glyph for '0': {cmap[48]}")

# The key is to find the relationship between the obfuscated character codes and the real characters.
# I will try to find a public, non-obfuscated version of a similar font.
# But I don't know what the original font is.

# Let's try a different approach.
# The text is rendered correctly in a browser. This means the browser has all the information it needs.
# The browser uses the font file and the character codes in the HTML to render the text.
# The font file provides the glyphs. The character codes in the HTML select which glyph to use.
# So, the mapping is from the character code in the HTML to a glyph in the font file.

# Let's assume the HTML contains characters like `&#xE123;`. This is a PUA character.
# The font file has a glyph for `U+E123`. This glyph looks like a real character, say 'A'.
# So, we need to find out which glyph corresponds to which real character.

# Let's try to get the glyph names and see if they give us a clue.
with open('glyph_names.txt', 'w', encoding='utf-8') as f:
    for name in glyph_names:
        f.write(name + '\n')

# I will now run this script. Then I will inspect the output files.
# After that, I will have a better idea of how to proceed.
print("Font parsing script finished.")
