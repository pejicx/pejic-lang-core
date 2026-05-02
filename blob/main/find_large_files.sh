#!/bin/bash
# Find files over 10 MB, use Copilot CLI to describe them, and email a summary

EMAIL_TO="user@example.com"
SUBJECT="Large file found"
BODY=""

while IFS= read -r -d '' file; do
    size=$(du -h "$file" | cut -f1)
    description=$(copilot -p "Describe this file briefly: $file" -s 2>/dev/null)
    BODY+="File: $file"$'\n'"Size: $size"$'\n'"Description:     $description"$'\n\n'
done < <(find . -type f -size +10M -print0)

if [ -z "$BODY" ]; then
    echo "No files over 10MB found."
    exit 0
fi

echo -e "To: $EMAIL_TO\nSubject: $SUBJECT\n\n$BODY" | sendmail "$EMAIL_TO"
echo "Email sent to $EMAIL_TO with large file details."
