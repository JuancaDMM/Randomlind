#!/usr/bin/env python3
"""
Script para generar manifest.json del modpack
Ejecuta esto en el directorio de tu servidor donde tienes los archivos del modpack
"""

import os
import json
import hashlib
from pathlib import Path
import argparse

def calculate_sha256(file_path):
    """Calcular SHA256 de un archivo"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(base_dir, version="1.0.1", mode="all", output_filename=None):
    """Generar manifest.json para el modpack.
    mode: 'all' (por defecto) incluye mods y recursos; 'configs' incluye solo configuración (config, scripts, defaultconfigs, kubejs).
    output_filename: nombre del archivo de salida, si no se especifica usa manifest.json o manifest-configs.json según el modo.
    """
    
    base_path = Path(base_dir)
    manifest = {
        "version": version,
        "minecraft_version": "1.16.5",
        "forge_version": "36.2.42",
        "files": []
    }
    
    # Directorios a incluir en el modpack según el modo
    if mode == 'configs':
        include_dirs = ['config', 'scripts', 'defaultconfigs', 'kubejs']
    else:
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
    if output_filename is None:
        output_filename = 'manifest-configs.json' if mode == 'configs' else 'manifest.json'
    manifest_path = base_path / output_filename
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"✅ Manifest generado: {manifest_path}")
    print(f"📊 Total de archivos: {len(manifest['files'])}")
    print(f"📦 Versión: {version}")
    
    return manifest

if __name__ == "__main__":
    import sys
    
    parser = argparse.ArgumentParser(description="Generador de manifest para modpack")
    parser.add_argument('modpack_dir', nargs='?', default='.', help='Directorio base del modpack (por defecto: .)')
    parser.add_argument('--version', default='1.0.0', help='Versión a escribir en el manifest')
    parser.add_argument('--mode', choices=['all', 'configs'], default='all', help='Modo de generación: all o configs')
    parser.add_argument('--output', default=None, help='Nombre del archivo de salida (opcional)')
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════╗
║   Generador de Manifest para Modpack            ║
║   Minecraft Launcher Auto-Actualizable          ║
╚══════════════════════════════════════════════════╝
""")
    
    try:
        generate_manifest(args.modpack_dir, args.version, args.mode, args.output)
        out_name = args.output or ('manifest-configs.json' if args.mode == 'configs' else 'manifest.json')
        print(f"\n🎉 ¡Listo! Sube {out_name} junto con tus archivos al servidor.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
