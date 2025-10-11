"""
Test intelligent message splitting functionality
"""
from bot import split_text_intelligently


def test_short_message():
    """Test that short messages are not split"""
    text = "This is a short message."
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    assert len(chunks) == 1
    assert chunks[0] == text
    print("✓ Short message test passed")


def test_sentence_boundary_split():
    """Test that long messages split at sentence boundaries"""
    # Create a message with clear sentence boundaries
    sentence1 = "This is the first sentence. " * 40  # ~1120 chars
    sentence2 = "This is the second sentence. " * 40  # ~1160 chars
    text = sentence1 + sentence2
    
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    
    # Should split into 2 chunks
    assert len(chunks) == 2
    
    # First chunk should end at a sentence boundary (with period)
    assert chunks[0].rstrip().endswith('.')
    
    # Second chunk should start with a capital letter (new sentence)
    assert chunks[1][0].isupper()
    
    print(f"✓ Sentence boundary split test passed - {len(chunks)} chunks")


def test_paragraph_boundary_split():
    """Test that messages split at paragraph boundaries when possible"""
    paragraph1 = "First paragraph. " * 60  # ~1020 chars
    paragraph2 = "\n\nSecond paragraph. " * 60  # ~1140 chars
    text = paragraph1 + paragraph2
    
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    
    # Should split at paragraph boundary
    assert len(chunks) == 2
    print(f"✓ Paragraph boundary split test passed - {len(chunks)} chunks")


def test_very_long_sentence():
    """Test that very long sentences (no boundaries) still split"""
    # Create a very long sentence with no periods
    text = "A" * 3000  # 3000 chars, no sentence boundaries
    
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    
    # Should split even without sentence boundaries
    assert len(chunks) >= 2
    
    # Each chunk should be <= 1900 chars
    for chunk in chunks:
        assert len(chunk) <= 1900
    
    print(f"✓ Very long sentence test passed - {len(chunks)} chunks")


def test_word_boundary_split():
    """Test that splits avoid breaking words when no sentence boundary"""
    # Create text with spaces but no sentence boundaries
    text = "word " * 500  # ~2500 chars, spaces but no periods
    
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    
    # Should split at word boundaries (spaces)
    assert len(chunks) >= 2
    
    # First chunk should end with "word" not "wo" (not split mid-word)
    assert chunks[0].rstrip().endswith('word')
    
    print(f"✓ Word boundary split test passed - {len(chunks)} chunks")


def test_mixed_content():
    """Test realistic mixed content with sentences and paragraphs"""
    text = """This is the first paragraph. It has multiple sentences. Each sentence is relatively short.

This is the second paragraph. It also has multiple sentences. """ * 20
    
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    
    # Should create multiple chunks
    assert len(chunks) >= 2
    
    # All chunks should be within limit
    for i, chunk in enumerate(chunks):
        assert len(chunk) <= 1900, f"Chunk {i} is {len(chunk)} chars (over limit)"
    
    # Each chunk should end cleanly (not mid-word)
    for chunk in chunks[:-1]:  # All but last chunk
        assert chunk.rstrip()[-1] in '.!?\n' or chunk.rstrip().endswith(' ')
    
    print(f"✓ Mixed content test passed - {len(chunks)} chunks")


def test_exact_boundary():
    """Test edge case where content is exactly at the boundary"""
    text = "A" * 1900
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    assert len(chunks) == 1
    print("✓ Exact boundary test passed")


def test_just_over_boundary():
    """Test content just over the boundary"""
    text = "A" * 1901
    chunks = split_text_intelligently(text, max_chunk_size=1900)
    assert len(chunks) == 2
    print("✓ Just over boundary test passed")


if __name__ == "__main__":
    print("Running intelligent message splitting tests...\n")
    
    test_short_message()
    test_sentence_boundary_split()
    test_paragraph_boundary_split()
    test_very_long_sentence()
    test_word_boundary_split()
    test_mixed_content()
    test_exact_boundary()
    test_just_over_boundary()
    
    print("\n✅ All tests passed!")
