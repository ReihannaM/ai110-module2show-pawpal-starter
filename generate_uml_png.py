"""
Script to generate UML diagram PNG from Mermaid file
This script helps convert uml_final.mmd to uml_final.png

Options:
1. Use Mermaid Live Editor (recommended for quick generation)
2. Install mermaid-cli globally (requires Node.js)
"""

import webbrowser
import urllib.parse


def open_mermaid_live():
    """Open Mermaid Live Editor with the diagram code"""
    print("Opening Mermaid Live Editor in your browser...")
    print("\nSteps:")
    print("1. The Mermaid Live Editor will open in your browser")
    print("2. Copy the contents of uml_final.mmd")
    print("3. Paste into the editor (it will auto-render)")
    print("4. Click the 'PNG' or 'SVG' button to download")
    print("5. Save as 'uml_final.png' in your project folder")
    print("\nOpening browser...")

    # Read the mermaid file
    try:
        with open('uml_final.mmd', 'r') as f:
            mermaid_code = f.read()

        # URL encode the code
        encoded_code = urllib.parse.quote(mermaid_code)

        # Open Mermaid Live Editor with the code
        url = f"https://mermaid.live/edit#pako:eNpVkE1rwzAMhv-K0WkbaGDX7dBLjz2MMRiDsUMP1pRkDk1SbJdRSv57lZQFdpP1vHokJL2Sb7UDK3mtRb-T4lWCEweVBQspSq30QDVYI7WGSjKC3kBdgRVKS2ggB68l2Eq1UKEy0EK70BoqZZRUFSTplVSQyQpspcFWuoOWKmlqVUMr"
        webbrowser.open("https://mermaid.live/")

        print("\n✅ Browser opened!")
        print("\n📋 Your Mermaid code is in 'uml_final.mmd'")
        print("   Copy and paste it into the editor that just opened.")

    except FileNotFoundError:
        print("❌ Error: uml_final.mmd not found!")
        print("   Make sure you're running this script from the project root directory.")


def show_cli_instructions():
    """Show instructions for using mermaid-cli"""
    print("\n" + "="*70)
    print("OPTION 2: Using Mermaid CLI (Command Line)")
    print("="*70)
    print("\nIf you have Node.js installed, you can use the command line:")
    print("\n1. Install mermaid-cli globally:")
    print("   npm install -g @mermaid-js/mermaid-cli")
    print("\n2. Generate PNG:")
    print("   mmdc -i uml_final.mmd -o uml_final.png")
    print("\n3. Or with custom dimensions:")
    print("   mmdc -i uml_final.mmd -o uml_final.png -w 2000 -H 1500")


def main():
    """Main function to guide user through PNG generation"""
    print("\n" + "="*70)
    print("PawPal+ UML Diagram PNG Generator")
    print("="*70)
    print("\nThis script will help you convert uml_final.mmd to uml_final.png")
    print("\nChoose an option:")
    print("  1. Open Mermaid Live Editor (easiest, recommended)")
    print("  2. Show CLI instructions (requires Node.js)")
    print("  3. Exit")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        open_mermaid_live()
    elif choice == "2":
        show_cli_instructions()
    elif choice == "3":
        print("\n👋 Goodbye!")
    else:
        print("\n❌ Invalid choice. Please run the script again.")

    print("\n" + "="*70)
    print("For detailed instructions, see UML_DIAGRAM.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
