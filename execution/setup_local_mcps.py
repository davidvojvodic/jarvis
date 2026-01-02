import json
import os
import sys
import platform

def get_mcp_config_path():
    """Attempts to find the MCP config file based on OS and standard locations."""
    system = platform.system()
    home = os.path.expanduser("~")
    
    # Define search paths based on likely agent/client setups
    # Antigravity usually uses a specific path in .gemini or AppData
    possible_paths = [
        # Windows
        os.path.join(home, ".gemini", "antigravity", "mcp_config.json"),
        os.path.join(os.environ.get("APPDATA", ""), "Antigravity", "mcp_config.json"),
        # Mac/Linux (Standard locations for Claude Desktop or similar)
        os.path.join(home, "Library", "Application Support", "Claude", "claude_desktop_config.json"),
        os.path.join(home, ".config", "Claude", "claude_desktop_config.json"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
            
    return None

def main():
    print(f"Detected OS: {platform.system()}")
    
    # 1. Location of THIS repository (where the script is running from)
    # Assuming this script is in 'jarvis/execution' or root 'jarvis'
    # We want the path to 'mcp-servers/flowko-knowledge'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle if running from root vs execution folder
    if "execution" in current_dir:
        repo_root = os.path.dirname(current_dir)
    else:
        repo_root = current_dir

    server_dir = os.path.join(repo_root, "mcp-servers", "flowko-knowledge")
    script_path = os.path.join(server_dir, "dist", "index.js")
    
    if not os.path.exists(script_path):
        print(f"❌ Error: Could not find MCP server at: {script_path}")
        print("Did you run 'npm run build' inside mcp-servers/flowko-knowledge?")
        sys.exit(1)

    print(f"✅ Found MCP Server at: {server_dir}")

    # 2. Find the Config File
    config_path = get_mcp_config_path()
    
    if not config_path:
        print("⚠️  Could not auto-detect mcp_config.json location.")
        config_path = input("Please paste the full path to your mcp_config.json: ").strip().strip('"')

    print(f"📂 Editing Config: {config_path}")

    # 3. Load Environment Variables from .env (Security Fix)
    env_path = os.path.join(repo_root, ".env")
    loaded_env = {}
    
    if os.path.exists(env_path):
        print(f"🔒 Loading secrets from: {env_path}")
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        loaded_env[key.strip()] = value.strip().strip('"').strip("'")
        except Exception as e:
            print(f"⚠️  Error reading .env: {e}")
    else:
        print("⚠️  No .env file found via auto-detection.")

    def get_env_var(key, default_value=""):
        """Get from .env or prompt user."""
        val = loaded_env.get(key)
        if val:
            return val
        # If not in .env, checking os.environ or asking user could be options, 
        # but for now we'll warn or leave empty to prompt user to fill .env
        print(f"⚠️  Missing {key} in .env file.")
        return input(f"Enter value for {key}: ").strip()

    # 4. Define Known Servers
    SERVERS = {
        "flowko-knowledge": {
            "path": os.path.join(server_dir, "flowko-knowledge", "dist", "index.js"),
            "dir": os.path.join(server_dir, "flowko-knowledge"),
            "env": {
                "SUPABASE_URL": get_env_var("SUPABASE_URL", ""),
                "SUPABASE_SERVICE_KEY": get_env_var("SUPABASE_SERVICE_KEY", ""),
                "VOYAGE_API_KEY": get_env_var("VOYAGE_API_KEY", "")
            }
        }
    }

    # 5. Update the Config
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        if "mcpServers" not in config:
            config["mcpServers"] = {}

        updated_count = 0
        for server_name, details in SERVERS.items():
            # Verify script exists
            if not os.path.exists(details["path"]):
                print(f"⚠️  Skipping {server_name}: Script not found at {details['path']}")
                continue

            config["mcpServers"][server_name] = {
                "command": "node",
                "args": [details["path"]],
                "cwd": details["dir"],
                "env": details["env"],
                "autoRestart": True
            }
            updated_count += 1
            print(f"✅ Configured '{server_name}'")

        if updated_count > 0:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"\n🎉 Successfully updated {updated_count} servers in {config_path}")
            print("🔄 Please RESTART your MCP Client/Agent to apply changes.")
        else:
            print("\n⚠️  No servers were updated (check paths).")

    except Exception as e:
        print(f"❌ Error writing config: {e}")

if __name__ == "__main__":
    main()
