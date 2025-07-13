import * as vscode from 'vscode';
import fetch from 'node-fetch';

export function activate(context: vscode.ExtensionContext) {
	let disposable = vscode.commands.registerCommand('derick.suggestCode', async () => {
		const editor = vscode.window.activeTextEditor;
		if (!editor) return;

		const document = editor.document;
		const position = editor.selection.active;

		const prompt = document.getText(new vscode.Range(
			new vscode.Position(Math.max(0, position.line - 10), 0),
			position
		));

		try {
			const res = await fetch("http://localhost:8000/complete", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ prompt })
			});

			const data = await res.json();

			editor.edit(editBuilder => {
				editBuilder.insert(position, data.completion || '⚠️ No response.');
			});
		} catch (error) {
			vscode.window.showErrorMessage("⚠️ Failed to fetch from Derick.");
		}
	});

	context.subscriptions.push(disposable);
}

export function deactivate() {}
