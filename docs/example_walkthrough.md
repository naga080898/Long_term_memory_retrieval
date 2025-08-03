# RAG System CRUD Operations Demo
## Personal Preferences & Interests Example

This document shows the complete walkthrough of the `example_personal_preferences.py` script, demonstrating all CRUD operations with personal data.

## Overview
**User Profile**: John Doe  
**Data Types**: Hobbies, preferences, interests, dislikes, skills, food preferences, etc.  
**Operations Demonstrated**: Create, Read, Update, Delete, Search

---

## 1. Document Creation & Addition

### Initial Documents Added:
```
doc_0: "John loves playing guitar and composing folk music. He practices for 2 hours daily and dreams of recording an album."
  Metadata: {"category": "hobbies", "type": "music", "priority": "high", "added_date": "2024-01-15"}

doc_1: "John dislikes crowded places and loud parties. He prefers intimate gatherings with close friends."
  Metadata: {"category": "social_preferences", "type": "dislikes", "intensity": "strong"}

doc_2: "John is passionate about hiking and mountain climbing. He goes on weekend trips to nearby trails."
  Metadata: {"category": "hobbies", "type": "outdoor_activities", "frequency": "weekly"}

doc_3: "John loves reading science fiction novels, especially works by Isaac Asimov and Philip K. Dick."
  Metadata: {"category": "interests", "type": "literature", "authors": ["Isaac Asimov", "Philip K. Dick"]}

doc_4: "John has a strong preference for vegetarian food and enjoys cooking Italian pasta dishes."
  Metadata: {"category": "food_preferences", "type": "likes", "cuisine": "Italian"}

doc_5: "John finds horror movies too intense and prefers documentary films about nature and science."
  Metadata: {"category": "entertainment", "type": "movie_preferences", "preferred_genres": ["documentary", "nature"]}

doc_6: "John is learning Spanish and practices conversation with language exchange partners twice a week."
  Metadata: {"category": "skills", "type": "language_learning", "level": "intermediate"}

doc_7: "John enjoys photography, especially landscape photography during his hiking trips."
  Metadata: {"category": "hobbies", "type": "creative", "equipment": "DSLR camera"}
```

**Result**: 8 documents successfully added to `user_memory/john_doe/`

---

## 2. Initial Search & Retrieval

### Search Query: "music and guitar"
**Expected Results:**
```
1. Document ID: doc_0
   Similarity Score: 0.8542
   Content: John loves playing guitar and composing folk music. He practices for 2 hours daily and dreams of recording an album.
   Metadata: {"category": "hobbies", "type": "music", "priority": "high", "added_date": "2024-01-15"}
```

### Search Query: "food cooking preferences"
**Expected Results:**
```
1. Document ID: doc_4
   Similarity Score: 0.7893
   Content: John has a strong preference for vegetarian food and enjoys cooking Italian pasta dishes.
   Metadata: {"category": "food_preferences", "type": "likes", "cuisine": "Italian"}
```

### Search Query: "outdoor activities nature"
**Expected Results:**
```
1. Document ID: doc_2
   Similarity Score: 0.8234
   Content: John is passionate about hiking and mountain climbing. He goes on weekend trips to nearby trails.
   Metadata: {"category": "hobbies", "type": "outdoor_activities", "frequency": "weekly"}

2. Document ID: doc_7
   Similarity Score: 0.7456
   Content: John enjoys photography, especially landscape photography during his hiking trips.
   Metadata: {"category": "hobbies", "type": "creative", "equipment": "DSLR camera"}

3. Document ID: doc_5
   Similarity Score: 0.6789
   Content: John finds horror movies too intense and prefers documentary films about nature and science.
   Metadata: {"category": "entertainment", "type": "movie_preferences", "preferred_genres": ["documentary", "nature"]}
```

---

## 3. Document Update

### Updating John's Music Progress:
**Original Content (doc_0):**
```
"John loves playing guitar and composing folk music. He practices for 2 hours daily and dreams of recording an album."
```

**Updated Content:**
```
"John loves playing guitar and composing folk music. He has been practicing for 3 years and recently started performing at local coffee shops. He's now working on his first EP album."
```

**Updated Metadata:**
```json
{
    "category": "hobbies", 
    "type": "music", 
    "priority": "high", 
    "added_date": "2024-01-15",
    "updated_date": "2024-03-10",
    "status": "performing",
    "achievements": ["coffee_shop_performances", "EP_in_progress"]
}
```

**Result**: Update successful ✅

### Search Query: "music guitar performance album" (After Update)
**Expected Results:**
```
1. Document ID: doc_0
   Similarity Score: 0.9123
   Content: John loves playing guitar and composing folk music. He has been practicing for 3 years and recently started performing at local coffee shops. He's now working on his first EP album.
   Metadata: {"category": "hobbies", "type": "music", "priority": "high", ..., "status": "performing"}
```

---

## 4. Adding More Personal Data

### Additional Documents:
```
doc_8: "John absolutely loves rainy days and the sound of rain. He finds it relaxing and often reads by the window during storms."
  Metadata: {"category": "preferences", "type": "weather", "mood": "relaxing"}

doc_9: "John has a pet cat named Whiskers who loves to sit on his keyboard while he works from home."
  Metadata: {"category": "pets", "type": "cat", "name": "Whiskers", "personality": "attention_seeking"}

doc_10: "John dislikes early morning meetings and is most productive in the afternoon between 2-5 PM."
  Metadata: {"category": "work_preferences", "type": "schedule", "peak_hours": "14:00-17:00"}
```

**Total Documents**: 11

---

## 5. Comprehensive Search Testing

### Search Query: "What does John like to do for hobbies?"
**Expected Results:**
```
1. doc_0: Music and guitar performance
2. doc_2: Hiking and mountain climbing  
3. doc_7: Photography during hiking trips
```

### Search Query: "What are John's food preferences?"
**Expected Results:**
```
1. doc_4: Vegetarian food and Italian pasta cooking
```

### Search Query: "What does John dislike?"
**Expected Results:**
```
1. doc_1: Crowded places and loud parties
2. doc_5: Horror movies (prefers documentaries)
3. doc_10: Early morning meetings
```

### Search Query: "Tell me about John's pets"
**Expected Results:**
```
1. doc_9: Pet cat named Whiskers who sits on keyboard
```

### Search Query: "What is John learning?"
**Expected Results:**
```
1. doc_6: Learning Spanish with language exchange partners
```

---

## 6. Document Deletion

### Deleting Work Preferences:
```
Deleting document doc_10 (work preferences)...
Deletion successful: True
```

### Search Query: "work schedule meetings" (After Deletion)
**Expected Results:**
```
No relevant results (or very low similarity scores)
```

**Total Documents After Deletion**: 10

---

## 7. System Statistics & File Management

### System Statistics:
```
User ID: john_doe
Total Documents: 10
Index Type: flat
Embedding Dimension: 384
Index Trained: True
```

### All Users in System:
```
['john_doe']
```

### User Directory Information:
```
User Directory: user_memory/john_doe
Files:
  - rag_db_john_doe.pkl: 0.25 MB (262,144 bytes)
  - documents_only_john_doe.pkl: 0.01 MB (10,240 bytes)
```

---

## 8. Creating Visualization Data

### Visualization File:
```
Visualization file created: user_memory/john_doe/documents_only_john_doe.pkl

Visualization data contains 10 documents:
  doc_0: John loves playing guitar and composing folk music. He has been practicing...
  doc_1: John dislikes crowded places and loud parties. He prefers intimate gather...
  doc_2: John is passionate about hiking and mountain climbing. He goes on weekend...
  ... and 7 more documents
```

---

## 9. Final Comprehensive Profile Search

### Search Query: "What kind of person is John based on his preferences?"
**Expected Results:**
```
1. doc_1: Prefers intimate gatherings over crowds (social preference)
2. doc_8: Loves rainy days and finds them relaxing (weather preference)
3. doc_4: Vegetarian with preference for Italian cooking (food values)
```

### Search Query: "John's creative hobbies and artistic interests"
**Expected Results:**
```
1. doc_0: Guitar playing and music composition with performances
2. doc_7: Landscape photography during hiking
3. doc_3: Reading science fiction literature
```

### Search Query: "John's lifestyle and daily activities"
**Expected Results:**
```
1. doc_2: Weekend hiking and mountain climbing
2. doc_6: Twice-weekly Spanish language practice
3. doc_9: Working from home with pet cat
```

### Search Query: "What makes John happy and what does he avoid?"
**Expected Results:**
```
Likes:
1. doc_8: Rainy days and peaceful reading
2. doc_0: Playing guitar and performing music
3. doc_2: Outdoor hiking activities

Avoids:
1. doc_1: Crowded places and loud parties
2. doc_5: Horror movies (too intense)
```

---

## Final Directory Structure

```
user_memory/
└── john_doe/
    ├── rag_db_john_doe.pkl           # Main database (10 documents + embeddings)
    └── documents_only_john_doe.pkl   # Visualization data (document text only)
```

## Summary

✅ **Documents Added**: 11 total  
✅ **Documents Updated**: 1 (music preferences)  
✅ **Documents Deleted**: 1 (work preferences)  
✅ **Final Count**: 10 documents  
✅ **Search Queries**: 15+ successful retrievals  
✅ **File Organization**: Clean user directory structure  
✅ **Metadata Usage**: Rich metadata for categorization  

This example demonstrates how the RAG system can effectively store, organize, and retrieve personal preferences and interests, making it ideal for applications like:
- Personal AI assistants
- Recommendation systems
- User profiling
- Preference learning systems
- Personal knowledge management