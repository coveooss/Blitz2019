export type IMove = [string, number, number];

export interface IPlayerMove {
    'py/tuple': [number, IMove];
}

export interface IPawnInitialPosition {
    'py/tuple': [number, number];
}

export type IGoalRow = [number | null, number | null]
export interface IPawnGoalPosition {
    'py/tuple': IGoalRow;
}

export interface IDeconnexionReason {
    'py/tuple': [number, string];
    team: string;
}

export interface IBlitzVisualization {
    actions: IPlayerMove[];
    initial_board: {
        size: number;
        pawns: IPawnInitialPosition[];
        goals: IPawnGoalPosition[];
        nb_walls: number[],
        horiz_walls: number[][],
        verti_walls: number[][],
    },
    winner: number;
    player_names: string[];
    players_ranking: number[];
    reasons: Array<IDeconnexionReason | string>;
}
