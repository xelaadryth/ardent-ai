#!/bin/bash
# Reusable output parsing functions for AI workflows

# Parse COMMIT_MESSAGE from output file
# Usage: parse_commit_message <output_file> <default_message>
parse_commit_message() {
    local output_file="$1"
    local default_message="$2"
    
    local commit_message=$(grep '^COMMIT_MESSAGE=' "$output_file" | head -n 1 | cut -d'=' -f2- | tr -d '\r')
    if [ -z "$commit_message" ]; then
        commit_message="$default_message"
    fi
    echo "$commit_message"
}

# Parse REQUEST_FILENAME from output file
# Usage: parse_request_filename <output_file>
parse_request_filename() {
    local output_file="$1"
    
    local request_filename=$(grep '^REQUEST_FILENAME=' "$output_file" | head -n 1 | cut -d'=' -f2- | tr -d '\r')
    echo "$request_filename"
}

# Generic parser for any variable from output file
# Usage: parse_variable <output_file> <variable_name>
parse_variable() {
    local output_file="$1"
    local variable_name="$2"
    
    local value=$(grep "^${variable_name}=" "$output_file" | head -n 1 | cut -d'=' -f2- | tr -d '\r')
    echo "$value"
}
