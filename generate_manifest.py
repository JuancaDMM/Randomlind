#!/usr/bin/env python3
"""
Script para generar manifest.json del modpack
Ejecuta esto en el directorio de tu servidor donde tienes los archivos del modpack
"""

import os
import json
import hashlib
from pathlib import Path

def calculate_sha256(file_path):
    """Calcular SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(base_dir, version="1.0.1"):
    """Generar manifest.json para el modpack"""
    
    base_path = Path(base_dir)
    manifest = {
        "version": version,
        "minecraft_version": "1.16.5",
        "forge_version": "36.2.42",
        "files": []
    }
    
    # Directorios a incluir en el modpack
    include_dirs = ['mods', 'config', 'scripts', 'defaultconfigs', 'kubejs', 'resourcepacks', 'shaderpacks', 'Randomsland Menu Stuff']
    
    print(f"Generando manifest para: {base_path}")
    print("=" * 50)
    
    for dir_name in include_dirs:
        dir_path = base_path / dir_name
        
        if not dir_path.exists():
            print(f"⚠️  Directorio {dir_name} no encontrado, omitiendo...")
            continue
        
        print(f"\n📁 Procesando {dir_name}/")
        
        # Buscar todos los archivos en el directorio
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                # Calcular ruta relativa
                relative_path = str(file_path.relative_to(base_path)).replace('\\', '/')
                
                # Calcular hash
                print(f"  🔍 {relative_path}...", end=" ")
                file_hash = calculate_sha256(file_path)
                file_size = file_path.stat().st_size
                
                manifest["files"].append({
                    "path": relative_path,
                    "sha256": file_hash,
                    "size": file_size
                })
                
                print(f"✅ ({file_size} bytes)")
    
    # Guardar manifest
    manifest_path = base_path / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"✅ Manifest generado: {manifest_path}")
    print(f"📊 Total de archivos: {len(manifest['files'])}")
    print(f"📦 Versión: {version}")
    
    return manifest

if __name__ == "__main__":
    import sys
    
    # Usar directorio actual o el especificado
    modpack_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"
    
    print("""
╔══════════════════════════════════════════════════╗
║   Generador de Manifest para Modpack            ║
║   Minecraft Launcher Auto-Actualizable          ║
╚══════════════════════════════════════════════════╝
""")
    
    try:
        generate_manifest(modpack_dir, version)
        print("\n🎉 ¡Listo! Sube manifest.json junto con tus archivos al servidor.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
