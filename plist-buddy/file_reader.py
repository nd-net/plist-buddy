import re, codecs, io, os

__all__ = ["read_lines"]

coding = re.compile(r"^[ \t\v]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")

def encoding_from_bom(line):
    if not line:
        return None
    boms = {
        codecs.BOM_UTF8: "utf-8",
        codecs.BOM_UTF32_LE: "utf-32-le",
        codecs.BOM_UTF32_BE: "utf-32-be",
        codecs.BOM_UTF16_LE: "utf-16-le",
        codecs.BOM_UTF16_BE: "utf-16-be",
    }
    for bom, name in boms.items():
        if line.startswith(bom):
            return codecs.lookup(name)
    return None
    
def encoding_from_comment(line):
    if not line:
        return None
    encodingValues = coding.findall(line)
    if not encodingValues:
        return None
    return codecs.lookup(encodingValues[-1])

def ensure_similar_codec(from_bom, from_comment):
    """
    Ensures that the codec from the BOM and from the comment are similar.
    They don't have to be exactly the same because the encoding in the BOM
    will contain a byte order mark, whereas the comment may use the shorthand form.
    """
    # use startswith here because utf-xx and utf-xx-[lb]e are different encodings;
    if from_bom != from_comment and not from_bom.name.startswith(from_comment.name):
        raise ValueError("The file encoding from the BOM is '{}', but there is a encoding comment specifying the encoding as '{}'.".format(from_bom.name, from_comment.name))
    

def get_incremental_decoder(encoding):
    return encoding.incrementaldecoder()
    
def decode(line, decoder):
    """
    Decodes a line with an incremental decoder and removes a Byte Order Mark if present.
    """
    text = decoder.decode(line)
    if text.startswith("\ufeff") or text.startswith("\ufffe"):
        return text[1:]
    else:
        return text

def read_lines(source, initial_encoding="utf-8"):
    """
    Reads lines from a given source file-like object opened in binary mode.
    Uses the encoding from the Unicode Byte Order Mark (BOM) and/or 
    specified by a PEP263 compatible encoding declaration in the first two lines:
    https://www.python.org/dev/peps/pep-0263/#defining-the-encoding
    
    If a file has both a BOM and an encoding declaration, then those two
    must match, otherwise this function raises a ValueError.
    
    If there is neither a BOM nor an encoding declaration, the function
    will use the initial_encoding if specified; if not it defaults to UTF-8.
    """
    iterator = iter(source)
    lines = [next(iterator, None) for _ in range(2)]
    
    from_bom = encoding_from_bom(lines[0])
    from_comment = None

    decoder = get_incremental_decoder(from_bom or codecs.lookup(initial_encoding or "utf-8"))
    
    for line in lines:
        if line is None:
            continue
        text = decode(line, decoder)
        
        # yield the text in the line decoded by the previous encoder any case
        yield text
        if from_comment:
            continue
        from_comment = encoding_from_comment(text)
        if not from_comment:
            continue
        # if there is a new encoding from the comment, 
        if from_bom:
            ensure_similar_codec(from_bom, from_comment)
            # keep the from_bom encoding
        else:
            decoder = get_incremental_decoder(from_comment)
    
    for line in iterator:
        yield decode(line, decoder)

