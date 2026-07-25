use std::collections::{BTreeSet, HashMap};
use std::env;
use std::fs;
use std::path::Path;
use std::process::ExitCode;

#[derive(Debug, Clone, PartialEq)]
struct SourceReference {
    title: String,
    locator: String,
}

#[derive(Debug, Clone, PartialEq)]
struct Concept {
    id: u64,
    title: String,
    summary: String,
    tags: Vec<String>,
    sources: Vec<SourceReference>,
}

#[derive(Debug, Clone, PartialEq)]
struct SearchHit {
    concept: Concept,
    score: f64,
    matched_fields: Vec<String>,
}

#[derive(Debug, Default)]
struct SearchIndex {
    concepts: Vec<Concept>,
}

impl SearchIndex {
    fn load(path: &Path) -> Result<Self, String> {
        let content = fs::read_to_string(path)
            .map_err(|error| format!("unable to read {}: {error}", path.display()))?;
        Self::parse(&content)
    }

    fn parse(content: &str) -> Result<Self, String> {
        let mut lines = content.lines();
        let header = lines.next().ok_or_else(|| "Atlas file is empty".to_string())?;
        if header != "ATLAS\t1" {
            return Err("unsupported or invalid Atlas header".to_string());
        }

        let mut concepts: HashMap<u64, Concept> = HashMap::new();
        let mut pending_sources: Vec<(u64, SourceReference)> = Vec::new();

        for (offset, line) in lines.enumerate() {
            let line_number = offset + 2;
            if line.trim().is_empty() {
                continue;
            }
            let fields = split_record(line)
                .map_err(|error| format!("line {line_number}: {error}"))?;
            match fields.first().map(String::as_str) {
                Some("C") => {
                    if fields.len() != 5 {
                        return Err(format!("line {line_number}: concept requires 5 fields"));
                    }
                    let id = parse_positive_id(&fields[1], line_number)?;
                    if fields[2].is_empty() {
                        return Err(format!("line {line_number}: concept title cannot be empty"));
                    }
                    let concept = Concept {
                        id,
                        title: fields[2].clone(),
                        summary: fields[3].clone(),
                        tags: fields[4]
                            .split('|')
                            .filter(|tag| !tag.is_empty())
                            .map(str::to_owned)
                            .collect(),
                        sources: Vec::new(),
                    };
                    if concepts.insert(id, concept).is_some() {
                        return Err(format!("line {line_number}: duplicate concept ID {id}"));
                    }
                }
                Some("S") => {
                    if fields.len() != 4 {
                        return Err(format!("line {line_number}: source requires 4 fields"));
                    }
                    let concept_id = parse_positive_id(&fields[1], line_number)?;
                    pending_sources.push((
                        concept_id,
                        SourceReference {
                            title: fields[2].clone(),
                            locator: fields[3].clone(),
                        },
                    ));
                }
                Some("R") => {
                    if fields.len() != 6 {
                        return Err(format!("line {line_number}: relation requires 6 fields"));
                    }
                    let _from = parse_positive_id(&fields[1], line_number)?;
                    let _to = parse_positive_id(&fields[2], line_number)?;
                    let weight: f64 = fields[4]
                        .parse()
                        .map_err(|_| format!("line {line_number}: invalid relation weight"))?;
                    if weight <= 0.0 {
                        return Err(format!("line {line_number}: relation weight must be positive"));
                    }
                }
                Some(record_type) => {
                    return Err(format!("line {line_number}: unknown record type {record_type:?}"));
                }
                None => return Err(format!("line {line_number}: empty record")),
            }
        }

        for (concept_id, source) in pending_sources {
            let concept = concepts
                .get_mut(&concept_id)
                .ok_or_else(|| format!("source references missing concept {concept_id}"))?;
            concept.sources.push(source);
        }

        let mut ordered: Vec<Concept> = concepts.into_values().collect();
        ordered.sort_by_key(|concept| concept.id);
        Ok(Self { concepts: ordered })
    }

    fn search(&self, query: &str, limit: usize) -> Vec<SearchHit> {
        let tokens = tokenize(query);
        if tokens.is_empty() || limit == 0 {
            return Vec::new();
        }

        let normalized_query = query.trim().to_lowercase();
        let mut results = Vec::new();
        for concept in &self.concepts {
            let title = concept.title.to_lowercase();
            let summary = concept.summary.to_lowercase();
            let mut score = if title == normalized_query { 12.0 } else { 0.0 };
            let mut fields = BTreeSet::new();

            for token in &tokens {
                if title.contains(token) {
                    score += 6.0;
                    fields.insert("title".to_string());
                    if title.starts_with(token) {
                        score += 1.0;
                    }
                }
                if summary.contains(token) {
                    score += 2.0;
                    fields.insert("summary".to_string());
                }
                if concept
                    .tags
                    .iter()
                    .any(|tag| tag.to_lowercase().contains(token))
                {
                    score += 4.0;
                    fields.insert("tags".to_string());
                }
                if concept.sources.iter().any(|source| {
                    source.title.to_lowercase().contains(token)
                        || source.locator.to_lowercase().contains(token)
                }) {
                    score += 1.0;
                    fields.insert("sources".to_string());
                }
            }

            if score > 0.0 {
                results.push(SearchHit {
                    concept: concept.clone(),
                    score,
                    matched_fields: fields.into_iter().collect(),
                });
            }
        }

        results.sort_by(|left, right| {
            right
                .score
                .total_cmp(&left.score)
                .then_with(|| left.concept.title.cmp(&right.concept.title))
                .then_with(|| left.concept.id.cmp(&right.concept.id))
        });
        results.truncate(limit);
        results
    }
}

fn parse_positive_id(value: &str, line_number: usize) -> Result<u64, String> {
    let id: u64 = value
        .parse()
        .map_err(|_| format!("line {line_number}: invalid positive ID {value:?}"))?;
    if id == 0 {
        return Err(format!("line {line_number}: IDs must be positive"));
    }
    Ok(id)
}

fn split_record(line: &str) -> Result<Vec<String>, String> {
    let mut fields = Vec::new();
    let mut field = String::new();
    let mut in_quotes = false;
    let mut escaped = false;

    for character in line.chars() {
        if escaped {
            field.push(character);
            escaped = false;
            continue;
        }
        if in_quotes {
            match character {
                '\\' => escaped = true,
                '"' => in_quotes = false,
                _ => field.push(character),
            }
            continue;
        }
        match character {
            '\t' => {
                fields.push(std::mem::take(&mut field));
            }
            '"' if field.is_empty() => in_quotes = true,
            _ => field.push(character),
        }
    }

    if escaped || in_quotes {
        return Err("unterminated quoted field".to_string());
    }
    fields.push(field);
    Ok(fields)
}

fn tokenize(value: &str) -> Vec<String> {
    value
        .to_lowercase()
        .split(|character: char| !character.is_alphanumeric())
        .filter(|token| !token.is_empty())
        .map(str::to_owned)
        .collect()
}

fn json_escape(value: &str) -> String {
    let mut output = String::with_capacity(value.len());
    for character in value.chars() {
        match character {
            '"' => output.push_str("\\\""),
            '\\' => output.push_str("\\\\"),
            '\n' => output.push_str("\\n"),
            '\r' => output.push_str("\\r"),
            '\t' => output.push_str("\\t"),
            character if character.is_control() => {
                output.push_str(&format!("\\u{:04x}", character as u32));
            }
            _ => output.push(character),
        }
    }
    output
}

fn print_json(query: &str, hits: &[SearchHit]) {
    print!(
        "{{\"query\":\"{}\",\"count\":{},\"results\":[",
        json_escape(query),
        hits.len()
    );
    for (index, hit) in hits.iter().enumerate() {
        if index != 0 {
            print!(",");
        }
        print!(
            "{{\"score\":{},\"matchedFields\":[",
            hit.score
        );
        for (field_index, field) in hit.matched_fields.iter().enumerate() {
            if field_index != 0 {
                print!(",");
            }
            print!("\"{}\"", json_escape(field));
        }
        print!(
            "],\"concept\":{{\"id\":{},\"title\":\"{}\",\"summary\":\"{}\",\"tags\":[",
            hit.concept.id,
            json_escape(&hit.concept.title),
            json_escape(&hit.concept.summary)
        );
        for (tag_index, tag) in hit.concept.tags.iter().enumerate() {
            if tag_index != 0 {
                print!(",");
            }
            print!("\"{}\"", json_escape(tag));
        }
        print!("],\"sources\":[");
        for (source_index, source) in hit.concept.sources.iter().enumerate() {
            if source_index != 0 {
                print!(",");
            }
            print!(
                "{{\"title\":\"{}\",\"locator\":\"{}\"}}",
                json_escape(&source.title),
                json_escape(&source.locator)
            );
        }
        print!("]}}}}");
    }
    println!("]}}");
}

fn usage(program: &str) {
    eprintln!("Usage: {program} <file.atlas> <query...> [--limit N]");
}

fn run() -> Result<(), String> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        usage(args.first().map(String::as_str).unwrap_or("atlas-search"));
        return Err("file and query are required".to_string());
    }

    let path = Path::new(&args[1]);
    let mut limit = 10usize;
    let mut query_parts = Vec::new();
    let mut index = 2usize;
    while index < args.len() {
        if args[index] == "--limit" {
            let raw_limit = args
                .get(index + 1)
                .ok_or_else(|| "--limit requires a value".to_string())?;
            limit = raw_limit
                .parse::<usize>()
                .map_err(|_| format!("invalid limit {raw_limit:?}"))?;
            index += 2;
        } else {
            query_parts.push(args[index].clone());
            index += 1;
        }
    }
    if query_parts.is_empty() {
        return Err("search query cannot be empty".to_string());
    }

    let query = query_parts.join(" ");
    let search_index = SearchIndex::load(path)?;
    let hits = search_index.search(&query, limit);
    print_json(&query, &hits);
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const SAMPLE: &str = concat!(
        "ATLAS\t1\n",
        "C\t1\t\"Knowledge Graph\"\t\"Connected knowledge\"\t\"graph|foundation\"\n",
        "S\t1\t\"Architecture\"\t\"docs/architecture.md\"\n",
        "C\t2\t\"Evidence\"\t\"Inspectable sources\"\t\"trust|research\"\n",
        "R\t2\t1\t\"supports\"\t1\t\"Evidence supports graphs\"\n",
    );

    #[test]
    fn splits_quoted_records_and_escapes() {
        let fields = split_record("C\t1\t\"A \\\"quoted\\\" title\"\t\"path \\\\ value\"\t\"x|y\"")
            .expect("record should parse");
        assert_eq!(fields[2], "A \"quoted\" title");
        assert_eq!(fields[3], "path \\ value");
    }

    #[test]
    fn parses_and_attaches_sources() {
        let index = SearchIndex::parse(SAMPLE).expect("sample should parse");
        assert_eq!(index.concepts.len(), 2);
        assert_eq!(index.concepts[0].sources.len(), 1);
    }

    #[test]
    fn ranks_title_and_tag_matches() {
        let index = SearchIndex::parse(SAMPLE).expect("sample should parse");
        let results = index.search("graph foundation", 10);
        assert_eq!(results[0].concept.id, 1);
        assert!(results[0].score > 10.0);
        assert!(results[0].matched_fields.contains(&"title".to_string()));
        assert!(results[0].matched_fields.contains(&"tags".to_string()));
    }

    #[test]
    fn rejects_missing_source_target() {
        let invalid = "ATLAS\t1\nS\t9\t\"Missing\"\t\"nowhere\"\n";
        let error = SearchIndex::parse(invalid).expect_err("source target should fail");
        assert!(error.contains("missing concept"));
    }
}
