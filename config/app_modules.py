# 2. config/app_modules.py (SOLO CONFIGURACIÓN)
"""
App Modules - Solo imports y configuración
"""

from src.feature.users.infrastructure.dependency_injection import UsersModule
# from src.feature.authentication.module import AuthModule  # Futuro


def configure_all_modules():
    """Configurar todos los modules - SOLO coordinación"""
    print("🔧 Configuring application modules...")

    UsersModule.configure()
    print("✅ Users module configured")

    # AuthModule.configure()
    # print("✅ Auth module configured")

    print("🎯 All modules configured successfully")

