function independent_lp_crosscheck(matrix_csv, weights_csv, output_csv)
% Independent CERT-Bench pairwise LP cross-check using MATLAB linprog.
% The input matrix must be tasks x methods with task names in column one.

matrix_table = readtable(matrix_csv, 'VariableNamingRule', 'preserve');
weight_table = readtable(weights_csv, 'VariableNamingRule', 'preserve');
method_names = string(matrix_table.Properties.VariableNames(2:end));
Z = table2array(matrix_table(:, 2:end));
w0 = weight_table{:, 'nominal_weight'};

assert(size(Z, 1) == numel(w0), 'Task/weight dimension mismatch');
assert(abs(sum(w0) - 1) <= 1e-12, 'Nominal weights do not sum to one');
assert(all(isfinite(Z), 'all'), 'Non-finite matrix entry');

[~, winner] = min(w0' * Z);
D = size(Z, 1);
M = size(Z, 2);
f = [zeros(D, 1); 0.5 * ones(D, 1)];
Aeq = [ones(1, D), zeros(1, D)];
beq = 1;
lb = zeros(2 * D, 1);
options = optimoptions('linprog', 'Display', 'none', 'Algorithm', 'dual-simplex');

rows = table('Size', [M - 1, 7], ...
    'VariableTypes', {'string','string','double','double','double','double','string'}, ...
    'VariableNames', {'winner','competitor','radius_tv','exitflag', ...
                      'boundary_residual','weight_sum_residual','status'});
position = 0;

for competitor = 1:M
    if competitor == winner
        continue
    end
    position = position + 1;
    Aabs = zeros(2 * D, 2 * D);
    babs = zeros(2 * D, 1);
    for task = 1:D
        Aabs(2 * task - 1, task) = 1;
        Aabs(2 * task - 1, D + task) = -1;
        babs(2 * task - 1) = w0(task);
        Aabs(2 * task, task) = -1;
        Aabs(2 * task, D + task) = -1;
        babs(2 * task) = -w0(task);
    end
    gap = Z(:, competitor) - Z(:, winner);
    A = [Aabs; gap', zeros(1, D)];
    b = [babs; 0];
    [x, objective, exitflag] = linprog(f, A, b, Aeq, beq, lb, [], options);
    rows.winner(position) = method_names(winner);
    rows.competitor(position) = method_names(competitor);
    rows.exitflag(position) = exitflag;
    if exitflag > 0
        rows.radius_tv(position) = objective;
        rows.boundary_residual(position) = max(gap' * x(1:D), 0);
        rows.weight_sum_residual(position) = abs(sum(x(1:D)) - 1);
        rows.status(position) = "PASS";
    else
        rows.radius_tv(position) = Inf;
        rows.boundary_residual(position) = NaN;
        rows.weight_sum_residual(position) = NaN;
        rows.status(position) = "INFEASIBLE";
    end
end

writetable(rows, output_csv);
end
