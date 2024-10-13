'use client'

interface RunDetailProps{
	runId: number | null;
}

export function RunDetail({runId}:RunDetailProps){
	if(runId !== null){
		return `${runId}`
	}
}