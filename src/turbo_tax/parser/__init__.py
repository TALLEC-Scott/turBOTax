"""IRS Document Parser Module."""

from turbo_tax.parser.models import DocumentType, ParsedDocument, Section, Table
from turbo_tax.parser.parser import IRSParser

__all__ = ["DocumentType", "IRSParser", "ParsedDocument", "Section", "Table"]
