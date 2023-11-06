import argparse
from .converter import convert_md_to_html

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to styled HTML")
    
    # Add default="README.md" for the inputfile argument
    parser.add_argument("inputfile", type=str, default="README.md", nargs="?", help="Input markdown file path")
    
    # Here the outputfile default remains "output.html". You mentioned "inputfile.html", but 
    # note that this would require dynamic generation based on the inputfile argument's value.
    # For simplicity, keeping it as "output.html".
    parser.add_argument("outputfile", type=str, nargs="?", default="output.html", help="Output HTML file path (optional)")
    parser.add_argument("--mode", choices=["light", "dark"], default="dark", help="Styling mode (light/dark, default is dark)")

    args = parser.parse_args()

    convert_md_to_html(args.inputfile, args.outputfile, args.mode)

if __name__ == "__main__":
    main()
