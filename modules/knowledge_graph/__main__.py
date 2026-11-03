"""模块入口：python -m modules.knowledge_graph"""
from modules.knowledge_graph import load_entries

if __name__ == "__main__":
    entries = load_entries()
    print(f"[KG] 已加载 {len(entries)} 条萍乡文化种子知识。")
    for e in entries[:3]:
        print(f" - [{e.get('category')}] {e.get('title')}")
