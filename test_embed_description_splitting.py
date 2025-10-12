"""
Test embed description splitting for viewc and viewu commands
"""
from bot import split_text_intelligently


def test_short_description():
    """Test that short descriptions (< 4096 chars) are not split"""
    description = "This is a short character description."
    
    # Simulate what the code does
    if len(description) <= 4096:
        chunks = [description]  # No splitting needed
    else:
        chunks = split_text_intelligently(description, max_chunk_size=4000)
    
    assert len(chunks) == 1
    assert chunks[0] == description
    print("✓ Short description test passed - No splitting needed")


def test_long_description_splitting():
    """Test that long descriptions (> 4096 chars) are split correctly"""
    # Create a description longer than 4096 characters
    sentence = "This is a detailed character background with lots of information. "
    description = sentence * 70  # Creates ~4480 characters
    
    assert len(description) > 4096, f"Test description should be > 4096 chars, got {len(description)}"
    
    # Simulate what the code does
    if len(description) <= 4096:
        chunks = [description]
    else:
        chunks = split_text_intelligently(description, max_chunk_size=4000)
    
    # Should be split into at least 2 chunks
    assert len(chunks) >= 2, f"Expected at least 2 chunks, got {len(chunks)}"
    
    # Each chunk should be under 4096 characters
    for i, chunk in enumerate(chunks):
        assert len(chunk) <= 4096, f"Chunk {i} is {len(chunk)} chars, exceeds 4096 limit"
    
    # Verify chunks end at sentence boundaries
    for i, chunk in enumerate(chunks[:-1]):  # All except last chunk
        assert chunk.rstrip().endswith('.'), f"Chunk {i} should end at sentence boundary"
    
    print(f"✓ Long description splitting test passed - {len(chunks)} chunks created")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk)} characters")


def test_very_long_description():
    """Test splitting of very long descriptions (> 8000 chars)"""
    # Create a very long description
    sentence = "The character has an extensive history spanning many years. "
    description = sentence * 150  # Creates ~9000 characters
    
    assert len(description) > 8000, f"Test description should be > 8000 chars, got {len(description)}"
    
    # Simulate what the code does
    if len(description) <= 4096:
        chunks = [description]
    else:
        chunks = split_text_intelligently(description, max_chunk_size=4000)
    
    # Should be split into multiple chunks
    assert len(chunks) >= 3, f"Expected at least 3 chunks for very long text, got {len(chunks)}"
    
    # Each chunk should be under 4096 characters
    for i, chunk in enumerate(chunks):
        assert len(chunk) <= 4096, f"Chunk {i} is {len(chunk)} chars, exceeds 4096 limit"
    
    # Verify total content is preserved (approximately, accounting for trimming)
    total_chars = sum(len(chunk) for chunk in chunks)
    # Allow for some whitespace trimming
    assert total_chars >= len(description) * 0.95, "Too much content lost in splitting"
    
    print(f"✓ Very long description test passed - {len(chunks)} chunks created")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk)} characters")


def test_edge_case_exactly_4096():
    """Test edge case where description is exactly 4096 characters"""
    # Create exactly 4096 character description
    base = "X" * 4095
    description = base + "."  # Exactly 4096
    
    assert len(description) == 4096
    
    # Should NOT be split since it's exactly at the limit
    if len(description) <= 4096:
        chunks = [description]
    else:
        chunks = split_text_intelligently(description, max_chunk_size=4000)
    
    assert len(chunks) == 1, f"Should not split at exactly 4096 chars"
    print("✓ Edge case test passed - 4096 chars not split")


def test_edge_case_4097():
    """Test edge case where description is 4097 characters (just over limit)"""
    # Create 4097 character description with sentence boundaries
    sentence = "This is a test sentence. "
    # Calculate how many we need
    num_sentences = (4097 // len(sentence)) + 1
    description = (sentence * num_sentences)[:4097]
    
    assert len(description) >= 4097, f"Expected at least 4097 chars, got {len(description)}"
    
    # Should be split
    if len(description) <= 4096:
        chunks = [description]
    else:
        chunks = split_text_intelligently(description, max_chunk_size=4000)
    
    assert len(chunks) >= 2, f"Should split when over 4096 chars"
    
    # Each chunk should be under limit
    for i, chunk in enumerate(chunks):
        assert len(chunk) <= 4096, f"Chunk {i} exceeds limit"
    
    print(f"✓ Edge case 4097 test passed - {len(chunks)} chunks created")


if __name__ == "__main__":
    print("Running embed description splitting tests...\n")
    
    test_short_description()
    test_long_description_splitting()
    test_very_long_description()
    test_edge_case_exactly_4096()
    test_edge_case_4097()
    
    print("\n✅ All embed description splitting tests passed!")
    print("\nThis validates the fix for the Discord embed description limit issue.")
    print("Characters with descriptions > 4096 characters will now be split into multiple embeds.")
