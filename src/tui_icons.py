"""
Icon constants for TUI applications.

Supports both Nerd Fonts (Material Design Icons) and Unicode fallbacks.
"""

# Nerd Fonts Material Design Icons
# These require a Nerd Font to be installed (e.g., FiraCode Nerd Font)
NERD_ICONS = {
    # Navigation
    "home": "\ue88a",  # mdi-home
    "search": "\ue8b6",  # mdi-magnify
    "computer": "\ue30a",  # mdi-desktop-mac
    "menu": "\ue5d2",  # mdi-menu
    "back": "\ue5c4",  # mdi-arrow-left
    "forward": "\ue5c8",  # mdi-arrow-right
    "refresh": "\ue5d5",  # mdi-refresh
    
    # Cloud & Infrastructure
    "cloud": "\ue2c7",  # mdi-cloud
    "cloud_upload": "\ue2c8",  # mdi-cloud-upload
    "cloud_download": "\ue2c9",  # mdi-cloud-download
    "server": "\ueb50",  # mdi-server
    "network": "\ueb77",  # mdi-network
    "database": "\ue1f8",  # mdi-database
    "storage": "\ue1db",  # mdi-harddisk
    
    # Kubernetes & Containers
    "kubernetes": "\ufd31",  # nf-mdi-kubernetes
    "docker": "\ue7b0",  # mdi-docker
    "container": "\ueb3d",  # mdi-container
    "openshift": "\ue7b2",  # mdi-openshift (check availability)
    
    # Status
    "check": "\ue5ca",  # mdi-check
    "error": "\ue000",  # mdi-alert-circle
    "warning": "\ue002",  # mdi-alert
    "info": "\ue88e",  # mdi-information
    "loading": "\ue863",  # mdi-loading
    
    # Actions
    "play": "\ue037",  # mdi-play
    "pause": "\ue036",  # mdi-pause
    "stop": "\ue047",  # mdi-stop
    "delete": "\ue872",  # mdi-delete
    "edit": "\ue3c9",  # mdi-pencil
    "add": "\ue145",  # mdi-plus
    "remove": "\ue15b",  # mdi-minus
}

# Unicode fallback icons (work in all terminals)
UNICODE_ICONS = {
    # Navigation
    "home": "⌂",
    "search": "🔍",
    "computer": "💻",
    "menu": "☰",
    "back": "←",
    "forward": "→",
    "refresh": "↻",
    
    # Cloud & Infrastructure
    "cloud": "☁",
    "cloud_upload": "☁↑",
    "cloud_download": "☁↓",
    "server": "🖥",
    "network": "🌐",
    "database": "🗄",
    "storage": "💾",
    
    # Kubernetes & Containers
    "kubernetes": "☸",
    "docker": "🐳",
    "container": "📦",
    "openshift": "⚙",
    
    # Status
    "check": "✓",
    "error": "✗",
    "warning": "⚠",
    "info": "ℹ",
    "loading": "⟳",
    
    # Actions
    "play": "▶",
    "pause": "⏸",
    "stop": "⏹",
    "delete": "🗑",
    "edit": "✎",
    "add": "+",
    "remove": "-",
}

# Rich emoji codes (for use with Rich library)
RICH_EMOJI = {
    "home": ":house:",
    "search": ":mag:",
    "computer": ":computer:",
    "cloud": ":cloud:",
    "server": ":desktop_computer:",
    "network": ":globe_with_meridians:",
    "database": ":file_cabinet:",
    "kubernetes": ":gear:",
    "docker": ":whale:",
    "check": ":white_check_mark:",
    "error": ":x:",
    "warning": ":warning:",
    "info": ":information:",
}


def get_icon(name: str, use_nerd_fonts: bool = True) -> str:
    """
    Get an icon by name.
    
    Args:
        name: Icon name (e.g., "home", "cloud", "kubernetes")
        use_nerd_fonts: If True, use Nerd Font icons (requires Nerd Font installed)
                       If False, use Unicode fallback
    
    Returns:
        Icon character(s) as string
    """
    if use_nerd_fonts and name in NERD_ICONS:
        return NERD_ICONS[name]
    return UNICODE_ICONS.get(name, "?")


def detect_nerd_fonts() -> bool:
    """
    Attempt to detect if Nerd Fonts are available.
    
    This is a simple heuristic - checks if a Nerd Font icon renders correctly.
    For production, you might want a more sophisticated detection method.
    
    Returns:
        True if Nerd Fonts appear to be available, False otherwise
    """
    try:
        # Try to render a Nerd Font icon
        test_icon = NERD_ICONS.get("cloud", "")
        # Simple check: if it's a single character and not a common Unicode char
        # This is a basic heuristic - you may want to improve this
        return len(test_icon) == 1 and ord(test_icon) > 0xE000
    except Exception:
        return False


# Auto-detect and create convenience dict
_USE_NERD = detect_nerd_fonts()
ICONS = NERD_ICONS if _USE_NERD else UNICODE_ICONS

# Convenience exports
__all__ = [
    "NERD_ICONS",
    "UNICODE_ICONS",
    "RICH_EMOJI",
    "get_icon",
    "detect_nerd_fonts",
    "ICONS",
]
